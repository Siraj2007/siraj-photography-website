# 📁 Gallery SOP — Sports Photography Website

## Purpose
This document defines how photos are added to the gallery, how `gallery.json` is structured, and how the frontend renders them.

---

## Source of Truth
`gallery.json` is the **only** file the frontend reads to display photos. It must always be valid JSON.

---

## gallery.json Schema

```json
{
  "last_updated": "YYYY-MM-DDTHH:MM:SS",
  "photos": [
    {
      "id": "uuid-string",
      "filename": "wm_photo.jpg",
      "category": "football",
      "title": "",
      "date_added": "YYYY-MM-DD",
      "orientation": "landscape"
    }
  ]
}
```

### Field Definitions
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | UUID, generated at upload time |
| `filename` | string | Watermarked filename with `wm_` prefix |
| `category` | enum | `football` | `floorball` | `general` |
| `title` | string | Optional display caption |
| `date_added` | string | ISO date (YYYY-MM-DD) |
| `orientation` | enum | `landscape` | `portrait` | `square` |

---

## Photo Storage Paths
```
images/football/wm_*.jpg
images/floorball/wm_*.jpg
images/general/wm_*.jpg
```

---

## Add Photo Workflow (Admin only)
1. Run `python tools/upload_handler.py`
2. Open `http://localhost:5000` in browser
3. Upload photo → select category → click Upload
4. Tool calls `watermark.py` → saves watermarked file to `images/{category}/`
5. Tool appends new entry to `gallery.json`
6. Frontend auto-reads updated `gallery.json` on next page load

---

## Remove Photo Workflow
> ⚠️ Manual step — no tool yet
1. Delete file from `images/{category}/`
2. Edit `gallery.json` — remove corresponding entry
3. Update `last_updated` timestamp

---

## Edge Cases
- **Duplicate filenames**: `upload_handler.py` appends timestamp to prevent collisions
- **Missing watermark file**: Falls back to text watermark `© Siraj Photography`
- **Corrupted gallery.json**: Backup created as `.tmp/gallery_backup_{timestamp}.json` before every write
