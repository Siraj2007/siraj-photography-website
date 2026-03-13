import os
import uuid
import json
import shutil
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont


def detect_orientation(img: Image.Image) -> str:
    w, h = img.size
    if w > h * 1.1:
        return "landscape"
    elif h > w * 1.1:
        return "portrait"
    else:
        return "square"


def apply_watermark(input_path: str, output_path: str, watermark_path: str = None) -> str:
    """
    Apply a watermark to a photo and save it to output_path.
    Falls back to a text watermark if watermark_path is not found.

    Args:
        input_path: Path to the source image
        output_path: Path where the watermarked image will be saved
        watermark_path: Path to a PNG watermark with alpha channel (optional)

    Returns:
        output_path on success
    """
    img = Image.open(input_path).convert("RGBA")
    img_w, img_h = img.size

    # --- Decide watermark mode ---
    if watermark_path and os.path.exists(watermark_path):
        # Mode 1: Image watermark
        wm = Image.open(watermark_path).convert("RGBA")

        # Scale watermark: width = 20% of photo width
        target_w = int(img_w * 0.20)
        ratio = target_w / wm.width
        target_h = int(wm.height * ratio)
        wm = wm.resize((target_w, target_h), Image.LANCZOS)

        # Apply 65% opacity
        r, g, b, a = wm.split()
        a = a.point(lambda x: int(x * 0.65))
        wm.putalpha(a)

        # Position: bottom-right with 20px padding
        pos_x = img_w - target_w - 20
        pos_y = img_h - target_h - 20

        # Paste watermark onto image
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        overlay.paste(wm, (pos_x, pos_y), wm)
        img = Image.alpha_composite(img, overlay)

    else:
        # Mode 2: Text watermark fallback
        draw = ImageDraw.Draw(img)
        text = "© Siraj Photography"
        font_size = max(20, img_w // 30)

        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        pos_x = img_w - text_w - 20
        pos_y = img_h - text_h - 20

        # Shadow for readability
        draw.text((pos_x + 2, pos_y + 2), text, font=font, fill=(0, 0, 0, 120))
        draw.text((pos_x, pos_y), text, font=font, fill=(255, 255, 255, 180))

    # Save as JPEG (convert from RGBA -> RGB first for JPEG compatibility)
    final = img.convert("RGB")
    final.save(output_path, "JPEG", quality=92)
    return output_path


if __name__ == "__main__":
    # Quick self-test
    import sys
    if len(sys.argv) < 3:
        print("Usage: python watermark.py <input_image> <output_image> [watermark_png]")
        sys.exit(1)

    input_p = sys.argv[1]
    output_p = sys.argv[2]
    wm_p = sys.argv[3] if len(sys.argv) > 3 else None

    result = apply_watermark(input_p, output_p, wm_p)
    print(f"Watermarked image saved to: {result}")
