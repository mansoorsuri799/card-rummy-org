(function () {
  const body = document.body;
  const menuBtn = document.querySelector("[data-menu-toggle]");
  const mobileNav = document.querySelector("[data-mobile-nav]");
  const langButtons = document.querySelectorAll("[data-lang]");

  function setLang(lang) {
    const next = lang === "ur" ? "ur" : "en";
    body.classList.remove("lang-en", "lang-ur");
    body.classList.add("lang-" + next);
    body.setAttribute("lang", next === "ur" ? "ur" : "en");
    body.setAttribute("dir", next === "ur" ? "rtl" : "ltr");
    langButtons.forEach(function (btn) {
      btn.setAttribute("aria-pressed", btn.getAttribute("data-lang") === next ? "true" : "false");
    });
    try {
      localStorage.setItem("cr-lang", next);
    } catch (e) {}
  }

  langButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      setLang(btn.getAttribute("data-lang"));
    });
  });

  let saved = "en";
  try {
    saved = localStorage.getItem("cr-lang") || "en";
  } catch (e) {}
  setLang(saved);

  if (menuBtn && mobileNav) {
    menuBtn.addEventListener("click", function () {
      const open = mobileNav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Lightbox for screenshot gallery
  const links = Array.prototype.slice.call(document.querySelectorAll("[data-lightbox]"));
  if (!links.length) return;

  const overlay = document.createElement("div");
  overlay.className = "lightbox";
  overlay.setAttribute("role", "dialog");
  overlay.setAttribute("aria-modal", "true");
  overlay.setAttribute("aria-label", "Image preview");
  overlay.innerHTML =
    '<div class="lightbox__panel">' +
    '<button type="button" class="lightbox__close" aria-label="Close">×</button>' +
    '<img src="" alt="">' +
    '<p class="lightbox__caption"></p>' +
    "</div>";
  document.body.appendChild(overlay);

  const img = overlay.querySelector("img");
  const caption = overlay.querySelector(".lightbox__caption");
  const closeBtn = overlay.querySelector(".lightbox__close");

  function currentLang() {
    return body.classList.contains("lang-ur") ? "ur" : "en";
  }

  function openLightbox(link) {
    const src = link.getAttribute("href");
    const altImg = link.querySelector("img");
    img.src = src;
    img.alt = altImg ? altImg.alt : "";
    const en = link.getAttribute("data-caption-en") || "";
    const ur = link.getAttribute("data-caption-ur") || en;
    caption.textContent = currentLang() === "ur" ? ur : en;
    overlay.classList.add("open");
    body.classList.add("lightbox-open");
    closeBtn.focus();
  }

  function closeLightbox() {
    overlay.classList.remove("open");
    body.classList.remove("lightbox-open");
    img.removeAttribute("src");
  }

  links.forEach(function (link) {
    link.addEventListener("click", function (event) {
      event.preventDefault();
      openLightbox(link);
    });
  });

  closeBtn.addEventListener("click", closeLightbox);
  overlay.addEventListener("click", function (event) {
    if (event.target === overlay) closeLightbox();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && overlay.classList.contains("open")) {
      closeLightbox();
    }
  });
})();
