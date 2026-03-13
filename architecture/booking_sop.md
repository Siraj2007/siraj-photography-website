# 📅 Booking SOP — Sports Photography Website

## Purpose
Defines the booking enquiry form, its fields, validation rules, and how the enquiry is delivered to Siraj.

---

## Delivery Method
**WhatsApp redirect** — No backend/email needed. On form submit, a `wa.me/` link opens with a pre-filled message. Siraj receives the enquiry directly in WhatsApp.

---

## Form Fields

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `name` | text | ✅ | Min 2 chars, letters + spaces only |
| `phone` | tel | ✅ | Must start with `+` and country code, digits only after |
| `location` | text | ✅ | Min 3 chars |
| `service` | dropdown | ✅ | Bronze | Silver | Gold |
| `sport` | dropdown | ✅ | Football | Floorball | Other |

> **Rule: NO EMAIL FIELD** — WhatsApp only.

---

## WhatsApp Message Format
On submit, the browser opens:
```
https://wa.me/{SIRAJ_WHATSAPP_NUMBER}?text=Hi+Siraj!+I'd+like+to+book+you.%0AName:+{name}%0APhone:+{phone}%0ALocation:+{location}%0AService:+{service}%0ASport:+{sport}
```

### Message Preview (rendered in WhatsApp)
```
Hi Siraj! I'd like to book you for a session.

Name: John Doe
Phone: +65 9123 4567
Location: Bishan Sports Hall
Service: Silver
Sport: Football
```

---

## Behavioral Rules
- All fields are required — submit button disabled until all fields filled
- Phone field shows placeholder: `+65 9123 4567`
- On successful submit: show a confirmation modal ("Your enquiry has been sent! Siraj will contact you shortly.")
- Booking form does NOT store data anywhere — it is a pure client-side redirect

---

## Future Phase Addition
- Integrate with Google Sheets to log all bookings
- Send automated WhatsApp confirmation to client
