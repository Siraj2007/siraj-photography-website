"""
upload_handler.py — Local Admin Upload Server
Run: python tools/upload_handler.py
Opens: http://localhost:5000
"""

import os
import sys
import uuid
import json
import shutil
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory

# Ensure tools/ imports work from anywhere
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from watermark import apply_watermark, detect_orientation

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR     = os.path.join(BASE_DIR, "images")
TMP_DIR        = os.path.join(BASE_DIR, ".tmp")
GALLERY_JSON   = os.path.join(BASE_DIR, "gallery.json")
WATERMARK_PATH = os.path.join(BASE_DIR, "watermark.png")
ALLOWED_EXT    = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}
CATEGORIES     = {"football", "floorball", "general"}

app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")

os.makedirs(TMP_DIR, exist_ok=True)


# ── Helpers ────────────────────────────────────────────────────────────────────

def load_gallery() -> dict:
    if not os.path.exists(GALLERY_JSON):
        return {"last_updated": "", "photos": []}
    with open(GALLERY_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def save_gallery(data: dict):
    # Backup before writing
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = os.path.join(TMP_DIR, f"gallery_backup_{ts}.json")
    if os.path.exists(GALLERY_JSON):
        shutil.copy2(GALLERY_JSON, backup)

    data["last_updated"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    with open(GALLERY_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/")
def serve_index():
    return send_from_directory(BASE_DIR, "index.html")


@app.route("/admin")
def serve_admin():
    return send_from_directory(BASE_DIR, "admin.html")


@app.route("/upload", methods=["POST"])
def upload_photo():
    if "photo" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file       = request.files["photo"]
    category   = request.form.get("category", "general").lower().strip()
    title      = request.form.get("title", "").strip()

    if category not in CATEGORIES:
        return jsonify({"error": f"Invalid category: {category}"}), 400

    # Check extension
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXT:
        return jsonify({"error": f"File type {ext} not allowed"}), 400

    # Save original to .tmp/
    ts          = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name   = f"{uuid.uuid4().hex}_{ts}{ext.lower()}"
    tmp_path    = os.path.join(TMP_DIR, safe_name)
    file.save(tmp_path)

    # Apply watermark
    wm_filename = f"wm_{safe_name.replace(ext.lower(), '.jpg')}"
    out_dir     = os.path.join(IMAGES_DIR, category)
    os.makedirs(out_dir, exist_ok=True)
    out_path    = os.path.join(out_dir, wm_filename)

    try:
        apply_watermark(tmp_path, out_path, WATERMARK_PATH)
    except Exception as e:
        return jsonify({"error": f"Watermark failed: {str(e)}"}), 500

    # Detect orientation from original
    from PIL import Image
    with Image.open(tmp_path) as img:
        orientation = detect_orientation(img)

    # Update gallery.json
    gallery = load_gallery()
    photo_entry = {
        "id":          str(uuid.uuid4()),
        "filename":    f"{category}/{wm_filename}",
        "category":    category,
        "title":       title,
        "date_added":  datetime.now().strftime("%Y-%m-%d"),
        "orientation": orientation
    }
    gallery["photos"].insert(0, photo_entry)  # newest first
    save_gallery(gallery)

    return jsonify({
        "result": {
            "original_file":       file.filename,
            "watermarked_file":    wm_filename,
            "saved_to":            f"images/{category}/{wm_filename}",
            "gallery_json_updated": True,
            "orientation":         orientation
        }
    })


@app.route("/gallery.json")
def serve_gallery():
    return send_from_directory(BASE_DIR, "gallery.json")


@app.route("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(IMAGES_DIR, filename)


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  📸 Siraj Photography — Admin Upload Server")
    print("=" * 55)
    print(f"  Admin panel : http://localhost:5000/admin")
    print(f"  Website     : http://localhost:5000")
    print(f"  Watermark   : {'✅ Found' if os.path.exists(WATERMARK_PATH) else '⚠️  Not found — using text fallback'}")
    print("=" * 55)
    app.run(debug=True, port=5000)
