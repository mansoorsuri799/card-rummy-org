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
})();
