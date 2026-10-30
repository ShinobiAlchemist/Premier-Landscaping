(function () {
  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.textContent = open ? "Close" : "Menu";
    });
  }

  // Review highlights: show or hide the items that still need Jose's confirmation
  var key = "plm-hide-review";
  var btn = document.querySelector("[data-toggle-review]");
  function apply(hidden) {
    document.body.classList.toggle("hide-tbd", hidden);
    if (btn) btn.textContent = hidden ? "Show items to confirm" : "Hide highlights";
  }
  var stored = false;
  try { stored = localStorage.getItem(key) === "1"; } catch (e) {}
  apply(stored);
  if (btn) {
    btn.addEventListener("click", function () {
      var hidden = !document.body.classList.contains("hide-tbd");
      apply(hidden);
      try { localStorage.setItem(key, hidden ? "1" : "0"); } catch (e) {}
    });
  }

  // Walkthrough request form (preview: not connected to email yet)
  var form = document.getElementById("walkthrough-form");
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var firstBad = null;
      form.querySelectorAll(".form-error").forEach(function (n) { n.remove(); });
      form.querySelectorAll("[required]").forEach(function (input) {
        input.removeAttribute("aria-invalid");
        if (!input.value.trim() || (input.type === "email" && !/^\S+@\S+\.\S+$/.test(input.value))) {
          input.setAttribute("aria-invalid", "true");
          var msg = document.createElement("p");
          msg.className = "form-error";
          msg.id = input.id + "-error";
          msg.textContent = input.type === "email" && input.value.trim()
            ? "Enter an email address like name@company.com."
            : "Fill in " + input.dataset.label + " so we can reach you.";
          input.setAttribute("aria-describedby", msg.id);
          input.insertAdjacentElement("afterend", msg);
          if (!firstBad) firstBad = input;
        }
      });
      if (firstBad) { firstBad.focus(); return; }
      var done = document.getElementById("form-done");
      form.hidden = true;
      done.hidden = false;
      done.querySelector("h2").focus();
    });
  }

  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();
})();
