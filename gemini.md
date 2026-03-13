# 📜 gemini.md — Project Constitution
## Siraj's Sports Photography Website | B.L.A.S.T. Protocol

> ⚠️ This file is LAW. Only update when: (1) schema changes, (2) a rule is added, (3) architecture is modified.

---

## 🗺️ Project Identity
- **Name:** Siraj's Sports Photography Website
- **Type:** Portfolio + Booking + Gallery Management
- **Protocol:** B.L.A.S.T. + A.N.T. 3-Layer Architecture
- **Status:** 🟡 Phase 1 — Blueprint Approved, Awaiting Build

---

## 🏛️ Architectural Invariants
1. LLMs (AI) handle routing and reasoning only — never deterministic business logic.
2. All business logic lives in atomic Python scripts under `tools/`.
3. Environment variables/secrets live ONLY in `.env` — never hardcoded.
4. All intermediate files go to `.tmp/` — never committed.
5. `gemini.md` is updated BEFORE the corresponding code changes.
6. The "Link" phase must pass before the "Architect" phase begins.
7. Frontend is **fully static** (HTML/CSS/JS) — no server required for visitors.
8. Admin upload panel is a **local Python Flask server** — only runs when Siraj adds photos.
9. All uploaded photos MUST have a watermark applied before being placed in `images/`.

---

## 📐 Data Schemas

### Photo Object (in gallery.json)
```json
{
  "id": "unique-string",
  "filename": "watermarked_filename.jpg",
  "category": "football | floorball | general",
  "title": "string (optional)",
  "date_added": "YYYY-MM-DD",
  "orientation": "landscape | portrait | square"
}
```

### gallery.json Structure (Source of Truth for frontend)
```json
{
  "last_updated": "YYYY-MM-DDTHH:MM:SS",
  "photos": [
    {
      "id": "uuid",
      "filename": "watermarked_photo.jpg",
      "category": "football",
      "title": "",
      "date_added": "YYYY-MM-DD",
      "orientation": "landscape"
    }
  ]
}
```

### Booking Form Input (collected from visitors)
```json
{
  "booking": {
    "name": "string (full name)",
    "phone": "string (WhatsApp number with country code)",
    "location": "string (venue / city)",
    "service": "string (package tier: Bronze | Silver | Gold)",
    "sport": "string (Football | Floorball | Other)"
  }
}
```

### Admin Upload Input (via local upload panel)
```json
{
  "upload": {
    "file": "binary (jpg/png/raw)",
    "category": "football | floorball | general",
    "title": "string (optional)"
  }
}
```

### Admin Upload Output (after processing)
```json
{
  "result": {
    "original_file": "filename.jpg",
    "watermarked_file": "wm_filename.jpg",
    "saved_to": "images/football/wm_filename.jpg",
    "gallery_json_updated": true
  }
}
```

---

## 📏 Behavioral Rules

| Rule | Description |
|------|-------------|
| WATERMARK | Every photo exported/uploaded MUST have the watermark applied. Watermark file to be provided by Siraj. |
| ORIENTATION | Photos can be any orientation (landscape, portrait, square). No filtering by orientation. |
| NO EMAIL | Booking form uses phone/WhatsApp only — no email field. |
| GALLERY AUTO-UPDATE | gallery.json is the single source of truth. Frontend reads it dynamically. Edited only by upload tool. |
| NO INTEGRATIONS (YET) | No external API calls in Phase 1. Everything is local. |
| PLACEHOLDER PRICING | Pricing packages use placeholder values until Siraj confirms real prices. |
| CATEGORIES | Three gallery categories: `football`, `floorball`, `general`. |

---

## 🔌 Integrations
| Service | Purpose | Status |
|---------|---------|--------|
| None    | All local for Phase 1 | ⏳ Future phases |

---

## 💰 Pricing Packages (Placeholder)
| Package | Duration | Deliverables | Price |
|---------|----------|--------------|-------|
| Bronze  | 1 hour   | 20 edited photos | TBD |
| Silver  | 2 hours  | 50 edited photos | TBD |
| Gold    | Half day | 100 edited photos + video clips | TBD |

---

## 📁 File Structure
```
├── index.html              # Main portfolio (Hero, About, Gallery, Pricing, Booking)
├── admin.html              # Admin upload panel (local use only)
├── gallery.json            # Auto-generated source of truth for gallery
├── css/
│   └── style.css           # Premium purple theme (vibrant accents)
├── js/
│   └── gallery.js          # Reads gallery.json, renders gallery + filters
├── images/
│   ├── football/           # Watermarked football photos
│   ├── floorball/          # Watermarked floorball photos
│   └── general/            # Watermarked general sports photos
├── tools/
│   ├── upload_handler.py   # Flask server: handles upload, watermark, gallery.json update
│   └── watermark.py        # Applies watermark to images (Pillow)
├── architecture/
│   ├── gallery_sop.md
│   ├── booking_sop.md
│   └── watermark_sop.md
├── .env                    # Secrets (future use)
├── .tmp/                   # Intermediate files
├── gemini.md               # This file (LAW)
├── task_plan.md
├── findings.md
└── progress.md
```

---

## 🔧 Maintenance Log
| Date | Change | Reason |
|------|--------|--------|
| 2026-03-13 | Initial constitution created | Protocol 0 Initialization |
| 2026-03-13 | Data Schema v1 defined | Discovery Questions answered — Blueprint phase |
