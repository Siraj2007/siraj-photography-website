/**
 * gallery.js — Dynamic gallery renderer
 * Reads gallery.json and renders photos with category filtering + lightbox
 */

const GALLERY_JSON = "./gallery.json";

let allPhotos = [];
let activeFilter = "all";
let lightboxIndex = 0;

// ── Init ──────────────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {
  fetchGallery();
  setupFilters();
  setupLightbox();
  setupBookingForm();
  setupNav();
});

// ── Fetch & Render ────────────────────────────────────────────────────────────

async function fetchGallery() {
  const grid = document.getElementById("gallery-grid");
  const empty = document.getElementById("gallery-empty");

  try {
    const res = await fetch(`${GALLERY_JSON}?t=${Date.now()}`);
    if (!res.ok) throw new Error("gallery.json not found");
    const data = await res.json();
    allPhotos = data.photos || [];
    renderGallery(activeFilter);
  } catch (err) {
    console.warn("Gallery load error:", err);
    if (empty) {
      empty.style.display = "flex";
      empty.innerHTML = `<p>📷 Gallery coming soon — check back after the next shoot!</p>`;
    }
    if (grid) grid.innerHTML = "";
  }
}

function renderGallery(filter) {
  const grid  = document.getElementById("gallery-grid");
  const empty = document.getElementById("gallery-empty");
  if (!grid) return;

  const filtered = filter === "all"
    ? allPhotos
    : allPhotos.filter(p => p.category === filter);

  if (filtered.length === 0) {
    grid.innerHTML = "";
    if (empty) {
      empty.style.display = "flex";
      empty.innerHTML = filter === "all"
        ? `<p>📷 Gallery coming soon — check back after the next shoot!</p>`
        : `<p>No ${filter} photos yet — check back soon!</p>`;
    }
    return;
  }

  if (empty) empty.style.display = "none";

  grid.innerHTML = filtered.map((photo, idx) => `
    <div class="gallery-item ${photo.orientation || 'landscape'}"
         data-index="${idx}"
         data-category="${photo.category}"
         onclick="openLightbox(${idx}, '${filter}')">
      <img
        src="images/${photo.filename}"
        alt="${photo.title || photo.category + ' photo'}"
        loading="lazy"
        onerror="this.parentElement.style.display='none'"
      />
      <div class="gallery-item-overlay">
        <span class="gallery-item-category">${capitalise(photo.category)}</span>
        ${photo.title ? `<span class="gallery-item-title">${photo.title}</span>` : ""}
      </div>
    </div>
  `).join("");
}

// ── Filters ───────────────────────────────────────────────────────────────────

function setupFilters() {
  const btns = document.querySelectorAll(".filter-btn");
  btns.forEach(btn => {
    btn.addEventListener("click", () => {
      btns.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      activeFilter = btn.dataset.filter;
      renderGallery(activeFilter);
    });
  });
}

// ── Lightbox ──────────────────────────────────────────────────────────────────

function setupLightbox() {
  const lb = document.getElementById("lightbox");
  if (!lb) return;

  document.getElementById("lightbox-close")?.addEventListener("click", closeLightbox);
  document.getElementById("lightbox-prev")?.addEventListener("click", () => shiftLightbox(-1));
  document.getElementById("lightbox-next")?.addEventListener("click", () => shiftLightbox(1));

  lb.addEventListener("click", e => {
    if (e.target === lb) closeLightbox();
  });

  document.addEventListener("keydown", e => {
    if (!lb.classList.contains("open")) return;
    if (e.key === "Escape")      closeLightbox();
    if (e.key === "ArrowLeft")   shiftLightbox(-1);
    if (e.key === "ArrowRight")  shiftLightbox(1);
  });
}

function openLightbox(idx, filter) {
  const filtered = filter === "all"
    ? allPhotos
    : allPhotos.filter(p => p.category === filter);

  lightboxIndex = idx;
  const photo = filtered[idx];
  const lb    = document.getElementById("lightbox");
  const img   = document.getElementById("lightbox-img");
  const cap   = document.getElementById("lightbox-caption");

  if (!lb || !img) return;

  img.src = `images/${photo.filename}`;
  if (cap) cap.textContent = photo.title || capitalise(photo.category);
  lb.classList.add("open");
  document.body.style.overflow = "hidden";

  // Store filtered list for nav
  lb.dataset.filter = filter;
}

function closeLightbox() {
  const lb = document.getElementById("lightbox");
  if (lb) lb.classList.remove("open");
  document.body.style.overflow = "";
}

function shiftLightbox(dir) {
  const lb     = document.getElementById("lightbox");
  const filter = lb?.dataset.filter || "all";
  const filtered = filter === "all"
    ? allPhotos
    : allPhotos.filter(p => p.category === filter);

  lightboxIndex = (lightboxIndex + dir + filtered.length) % filtered.length;
  openLightbox(lightboxIndex, filter);
}

// ── Booking Form ──────────────────────────────────────────────────────────────

function setupBookingForm() {
  const form = document.getElementById("booking-form");
  if (!form) return;

  form.addEventListener("submit", e => {
    e.preventDefault();

    const name     = document.getElementById("b-name")?.value.trim();
    const phone    = document.getElementById("b-phone")?.value.trim();
    const location = document.getElementById("b-location")?.value.trim();
    const service  = document.getElementById("b-service")?.value;
    const sport    = document.getElementById("b-sport")?.value;

    if (!name || !phone || !location || !service || !sport) {
      showFormError("Please fill in all fields.");
      return;
    }

    const message = encodeURIComponent(
      `Hi Siraj! I'd like to book you for a session.\n\n` +
      `Name: ${name}\n` +
      `Phone: ${phone}\n` +
      `Location: ${location}\n` +
      `Service: ${service}\n` +
      `Sport: ${sport}`
    );

    // Replace with Siraj's actual WhatsApp number
    const waNumber = "6591234567";
    window.open(`https://wa.me/${waNumber}?text=${message}`, "_blank");

    showBookingConfirmation();
    form.reset();
  });
}

function showFormError(msg) {
  const err = document.getElementById("form-error");
  if (err) {
    err.textContent = msg;
    err.style.display = "block";
    setTimeout(() => (err.style.display = "none"), 3500);
  }
}

function showBookingConfirmation() {
  const modal = document.getElementById("booking-modal");
  if (modal) {
    modal.classList.add("open");
    setTimeout(() => modal.classList.remove("open"), 4000);
  }
}

// ── Nav ───────────────────────────────────────────────────────────────────────

function setupNav() {
  // Hamburger toggle
  const hamburger = document.getElementById("hamburger");
  const navLinks  = document.getElementById("nav-links");
  hamburger?.addEventListener("click", () => {
    navLinks?.classList.toggle("open");
    hamburger.classList.toggle("active");
  });

  // Close mobile nav on link click
  document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
      navLinks?.classList.remove("open");
      hamburger?.classList.remove("active");
    });
  });

  // Sticky nav highlight on scroll
  const sections = document.querySelectorAll("section[id]");
  window.addEventListener("scroll", () => {
    let current = "";
    sections.forEach(section => {
      if (window.scrollY >= section.offsetTop - 80) {
        current = section.id;
      }
    });
    document.querySelectorAll(".nav-link").forEach(link => {
      link.classList.toggle("active", link.getAttribute("href") === `#${current}`);
    });
  }, { passive: true });
}

// ── Utility ───────────────────────────────────────────────────────────────────

function capitalise(str) {
  return str ? str.charAt(0).toUpperCase() + str.slice(1) : "";
}
