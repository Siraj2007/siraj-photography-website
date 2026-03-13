# 🖼️ Watermark SOP — Sports Photography Website

## Purpose
Every photo uploaded via the admin panel MUST have a watermark applied. This SOP defines watermark placement, sizing, opacity, and fallback behavior.

---

## Rule
> **INVARIANT**: No unwatermarked photo may ever be saved to `images/`. This is enforced by `upload_handler.py`, which always calls `watermark.py` before saving.

---

## Watermark Modes

### Mode 1: Image Watermark (Production)
- Watermark file: `watermark.png` (to be provided by Siraj)
- Must be a PNG with transparency (alpha channel)
- Placement: **Bottom-right corner**
- Padding from edge: 20px on each side
- Opacity: **65%** (blended, not opaque)
- Scale: Watermark is auto-scaled so its width = 20% of photo width

### Mode 2: Text Watermark (Fallback / Current)
- Triggered when `watermark.png` does not exist
- Text: `© Siraj Photography`
- Font: PIL default (or custom TTF if available)
- Placement: **Bottom-right corner**
- Color: White with 60% opacity
- Font size: Proportional to image width (width / 20)

---

## Orientation Handling
- **Landscape** (width > height): Standard placement applies
- **Portrait** (height > width): Standard placement applies, scale adjusts to 20% of width
- **Square**: Standard placement applies

---

## File Naming Convention
- Input: `photo.jpg`
- Output: `wm_photo_{timestamp}.jpg`
- Timestamp prevents filename collisions

---

## Tool Reference
- Script: `tools/watermark.py`
- Dependency: `Pillow` (`pip install pillow`)
- Function: `apply_watermark(input_path, output_path, watermark_path=None)`

---

## Swapping to Real Watermark
1. Place your watermark PNG at `watermark.png` in the project root
2. No code changes needed — `watermark.py` auto-detects it at the project root
3. Re-upload any photos you want re-watermarked via the admin panel

---

## Maintenance Log
| Date | Change | Reason |
|------|--------|--------|
| 2026-03-13 | SOP created | Phase 3 build |
