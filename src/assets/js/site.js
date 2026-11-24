// H&H Builders demo — progressive enhancement only; every page works without JS.
document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
  // Mobile nav
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = document.getElementById("primary-nav");
  if (toggle && nav) {
    const close = () => { toggle.setAttribute("aria-expanded", "false"); nav.classList.remove("is-open"); };
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") !== "true";
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { close(); toggle.focus(); }
    });
  }

  // Header border once scrolled
  const header = document.querySelector("[data-header]");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  // Before/after: hover on pointer devices (CSS), plus a real toggle button for keyboard/touch.
  document.querySelectorAll("[data-ba]").forEach((fig) => {
    const btn = fig.querySelector(".ba__toggle");
    if (!btn) return;
    btn.hidden = false;
    btn.addEventListener("click", () => {
      const on = btn.getAttribute("aria-pressed") !== "true";
      btn.setAttribute("aria-pressed", String(on));
      btn.textContent = on ? "Show after" : "Show before";
      fig.classList.toggle("is-before", on);
    });
  });

  // Project filter
  document.querySelectorAll("[data-filter]").forEach((group) => {
    const buttons = group.querySelectorAll("button");
    const items = document.querySelectorAll("[data-filter-item]");
    const status = document.querySelector("[data-filter-status]");
    buttons.forEach((b) => b.addEventListener("click", () => {
      const f = b.dataset.value;
      buttons.forEach((x) => x.setAttribute("aria-pressed", String(x === b)));
      let n = 0;
      items.forEach((it) => {
        const show = f === "all" || it.dataset.filterItem.split(" ").includes(f);
        it.hidden = !show; if (show) n++;
      });
      if (status) status.textContent = `Showing ${n} project${n === 1 ? "" : "s"}`;
    }));
    const preset = new URLSearchParams(location.search).get("type");
    const match = preset && group.querySelector(`button[data-value="${CSS.escape(preset)}"]`);
    if (match) match.click();
  });

  // Demo forms: no data leaves the page.
  document.querySelectorAll("form[data-demo-form]").forEach((form) => {
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      const thanks = form.querySelector(".form__thanks");
      form.querySelectorAll(".field, button[type=submit], .form__note").forEach((el) => (el.hidden = true));
      if (thanks) { thanks.hidden = false; thanks.focus(); }
    });
  });
});
