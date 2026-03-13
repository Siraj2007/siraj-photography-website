# 📋 Task Plan — Siraj's Sports Photography Website (B.L.A.S.T.)

## Status: 🟡 Phase 1 Blueprint — Pending User Approval

---

## Phase 0: Initialization ✅

- [x] Create `task_plan.md`
- [x] Create `findings.md`
- [x] Create `progress.md`
- [x] Initialize `gemini.md`
- [x] 5 Discovery Questions answered
- [x] Define JSON Data Schema in `gemini.md`
- [x] Blueprint implementation plan created

---

## Phase 1: B — Blueprint ✅ (Awaiting Approval)

- [x] Define North Star: Sports photography portfolio + booking + gallery
- [x] Confirm no integrations for Phase 1
- [x] Source of Truth: Local machine → `gallery.json` → static frontend
- [x] Delivery: Auto-update gallery via admin upload panel (Python Flask)
- [x] Behavioral Rules: Watermark all exports, any orientation, WhatsApp booking only
- [x] Confirm categories: football (primary), floorball (rare), general
- [x] Placeholder pricing: Bronze / Silver / Gold
- [x] Data Schema confirmed in `gemini.md`
- [ ] ⏳ USER APPROVAL of Blueprint

---

## Phase 2: L — Link ✅ (SKIPPED)

- [x] No external APIs in Phase 1 — Link phase not applicable

---

## Phase 3: A — Architect (Build)

- [ ] Create folder structure (images/, css/, js/, tools/, architecture/, .tmp/)
- [ ] Write SOPs:
  - [ ] `architecture/gallery_sop.md`
  - [ ] `architecture/booking_sop.md`
  - [ ] `architecture/watermark_sop.md`
- [ ] Build `tools/watermark.py` (Pillow-based watermark applicator)
- [ ] Build `tools/upload_handler.py` (Flask admin upload + gallery.json updater)
- [ ] Initialize `gallery.json` (empty, valid structure)

---

## Phase 4: S — Stylize (Frontend)

- [ ] Build `index.html` with sections:
  - [ ] Hero (dramatic full-screen banner)
  - [ ] About Me
  - [ ] Gallery (with filter: All / Football / Floorball / General)
  - [ ] Pricing (Bronze / Silver / Gold cards)
  - [ ] Booking Form (Name, WhatsApp, Location, Service, Sport)
  - [ ] Footer
- [ ] Build `admin.html` (local upload interface)
- [ ] Build `css/style.css` (premium dark sports theme)
- [ ] Build `js/gallery.js` (dynamic gallery from gallery.json + filters)

---

## Phase 5: T — Trigger (Finalize)

- [ ] Test full upload flow (upload → watermark → gallery.json → gallery renders)
- [ ] Validate booking form UI and data
- [ ] Add placeholder photos for demo
- [ ] Finalize Maintenance Log in `gemini.md`
- [ ] Present final result to user
