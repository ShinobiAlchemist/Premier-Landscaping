(function () {
  "use strict";

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

  // Review highlights
  var key = "plm-hide-review";
  var reviewBtn = document.querySelector("[data-toggle-review]");
  function applyReview(hidden) {
    document.body.classList.toggle("hide-tbd", hidden);
    if (reviewBtn) reviewBtn.textContent = hidden ? "Show items to confirm" : "Hide highlights";
  }
  var stored = false;
  try { stored = localStorage.getItem(key) === "1"; } catch (e) {}
  applyReview(stored);
  if (reviewBtn) {
    reviewBtn.addEventListener("click", function () {
      var hidden = !document.body.classList.contains("hide-tbd");
      applyReview(hidden);
      try { localStorage.setItem(key, hidden ? "1" : "0"); } catch (e) {}
    });
  }

  // Irrigation plan: zone buttons and clickable zones
  var plan = document.getElementById("plan");
  var note = document.getElementById("zone-note");
  var zoneNotes = {
    z1: "Zone 1, turf spray. Heads are checked for coverage and overspray, and run times change each month with the season.",
    z2: "Zone 2, parking island drip. Emitters at each island tree are checked monthly, so the trees get deep water without runoff onto the lot.",
    z3: "Zone 3, shrub bed drip. Clogged or missing emitters are replaced, with checks more often through the summer.",
    z4: "Zone 4, street tree bubblers. Slow, deep watering for street trees, adjusted after monsoon rain."
  };
  if (plan && note) {
    var defaultNote = note.textContent;
    var zoneBtns = document.querySelectorAll(".zones button");
    var setZone = function (z) {
      var current = plan.getAttribute("data-active");
      if (z && z === current) z = null;
      if (z) plan.setAttribute("data-active", z); else plan.removeAttribute("data-active");
      zoneBtns.forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.zone === z ? "true" : "false"); });
      note.textContent = z ? zoneNotes[z] : defaultNote;
    };
    zoneBtns.forEach(function (b) {
      b.addEventListener("click", function () { setZone(b.dataset.zone); });
    });
    plan.querySelectorAll(".zone").forEach(function (g) {
      g.addEventListener("click", function () { setZone(g.dataset.zone); });
    });
  }

  // Seasonal calendar: highlight the current month
  var monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  var monthWork = [
    "Frost protection on tender plants, dormant pruning of deciduous trees, and controllers on winter schedules.",
    "Pre-emergent for spring weeds, rose and perennial cutbacks, and an irrigation check as growth resumes.",
    "Spring planting, shrub pruning after the last frost, and controllers stepped up.",
    "A full irrigation check, zone by zone, and the first feeding as bermuda greens up.",
    "The transition from winter rye to bermuda, and pre-monsoon tree thinning.",
    "Early crew starts for heat safety, palm trimming after flowering, and longer run times.",
    "Monsoon readiness, storm cleanup as needed, and basin and drainage inlets kept clear.",
    "Storm response, irrigation adjusted after heavy rain, and the last of the palm trimming.",
    "Scalping bermuda, fall pre-emergent and storm damage repairs.",
    "Overseeding winter rye, the start of fall planting, and shorter run times.",
    "Mowing the new rye, fall planting, and holiday color for retail centers and entries.",
    "Frost cloth on hand, controllers moved to winter schedules, and a year-end walkthrough to plan next year."
  ];
  var now = new Date();
  var m = now.getMonth() + 1;
  document.querySelectorAll(".season[data-months]").forEach(function (s) {
    if (s.dataset.months.split(" ").indexOf(String(m)) > -1) s.classList.add("current");
  });
  var strip = document.getElementById("now-strip");
  if (strip) {
    var t = document.getElementById("now-month");
    t.textContent = monthNames[m - 1];
    t.setAttribute("datetime", now.getFullYear() + "-" + String(m).padStart(2, "0"));
    document.getElementById("now-work").textContent = "On Premier properties this month: " + monthWork[m - 1].charAt(0).toLowerCase() + monthWork[m - 1].slice(1);
    strip.hidden = false;
  }
  var row = document.querySelector('.month[data-month="' + m + '"]');
  if (row) row.classList.add("current");

  // Glossary popovers: place each one next to the term that opened it
  var lastTerm = null;
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".term");
    if (b) lastTerm = b;
  }, true);
  document.querySelectorAll("[popover].def").forEach(function (pop) {
    pop.addEventListener("toggle", function (e) {
      if (e.newState !== "open" || !lastTerm) return;
      var r = lastTerm.getBoundingClientRect();
      var w = Math.min(352, window.innerWidth - 24);
      pop.style.width = w + "px";
      var left = Math.max(12, Math.min(r.left, window.innerWidth - w - 12));
      var below = r.bottom + 8;
      var h = pop.offsetHeight;
      var top = below + h > window.innerHeight - 12 ? Math.max(12, r.top - h - 8) : below;
      pop.style.left = left + "px";
      pop.style.top = top + "px";
    });
  });
  window.addEventListener("scroll", function () {
    document.querySelectorAll("[popover].def").forEach(function (p) {
      try { if (p.matches(":popover-open")) p.hidePopover(); } catch (e) {}
    });
  }, { passive: true });

  // Full sample report dialog
  var dlg = document.getElementById("report-dialog");
  var openBtn = document.querySelector("[data-open-report]");
  if (dlg && openBtn && typeof dlg.showModal === "function") {
    openBtn.addEventListener("click", function () { dlg.showModal(); });
    dlg.querySelector("[data-close-report]").addEventListener("click", function () { dlg.close(); });
    dlg.addEventListener("click", function (e) { if (e.target === dlg) dlg.close(); });
    dlg.querySelector("[data-print-report]").addEventListener("click", function () {
      document.body.classList.add("printing-report");
      window.print();
    });
    window.addEventListener("afterprint", function () { document.body.classList.remove("printing-report"); });
  } else if (openBtn) {
    openBtn.hidden = true;
  }

  // Before and after slider
  var cmp = document.getElementById("compare");
  if (cmp) {
    var range = cmp.querySelector("input[type=range]");
    var update = function () {
      cmp.style.setProperty("--pos", range.value + "%");
      range.setAttribute("aria-valuetext", range.value + " percent showing after");
    };
    range.addEventListener("input", update);
    update();
  }

  // Proposal request form
  var form = document.getElementById("proposal-form");
  if (form) {
    var type = document.getElementById("type");
    var followups = form.querySelectorAll(".followup");
    type.addEventListener("change", function () {
      followups.forEach(function (f) { f.hidden = f.dataset.for !== type.value; });
    });

    var acres = document.getElementById("acres");
    var acresOut = document.getElementById("acres-out");
    var unknown = document.getElementById("acres-unknown");
    var showAcres = function () {
      if (unknown.checked) { acresOut.textContent = "Not sure"; acres.disabled = true; return; }
      acres.disabled = false;
      var v = parseFloat(acres.value);
      acresOut.textContent = (v >= 40 ? "40+ acres" : v + (v === 1 ? " acre" : " acres"));
    };
    acres.addEventListener("input", showAcres);
    unknown.addEventListener("change", showAcres);
    showAcres();

    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var firstBad = null;
      form.querySelectorAll(".form-error").forEach(function (n) { n.remove(); });
      form.querySelectorAll("[required]").forEach(function (input) {
        input.removeAttribute("aria-invalid");
        input.removeAttribute("aria-describedby");
        var empty = !input.value.trim();
        var badEmail = input.type === "email" && !empty && !/^\S+@\S+\.\S+$/.test(input.value);
        if (empty || badEmail) {
          input.setAttribute("aria-invalid", "true");
          var msg = document.createElement("p");
          msg.className = "form-error";
          msg.id = input.id + "-error";
          msg.textContent = badEmail ? "Enter an email address like name@company.com." : "Fill in " + input.dataset.label + " so we can reach you.";
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

  // Live Phoenix weather from the National Weather Service (Sky Harbor, KPHX)
  var wx = document.getElementById("wx");
  if (wx && window.fetch) {
    var icons = {
      sun: '<svg viewBox="0 0 36 36"><circle cx="18" cy="18" r="7" fill="#e4b93c"/><g stroke="#e4b93c" stroke-width="2.4" stroke-linecap="round"><path d="M18 3v4M18 29v4M3 18h4M29 18h4M7.4 7.4l2.8 2.8M25.8 25.8l2.8 2.8M7.4 28.6l2.8-2.8M25.8 10.2l2.8-2.8"/></g></svg>',
      moon: '<svg viewBox="0 0 36 36"><path d="M24 26a10 10 0 0 1-9.6-15.6A10 10 0 1 0 26.8 23 10 10 0 0 1 24 26z" fill="#b08a5a"/></svg>',
      partly: '<svg viewBox="0 0 36 36"><circle cx="13" cy="13" r="6" fill="#e4b93c"/><path d="M12 29h14a5.5 5.5 0 0 0 0-11 7.5 7.5 0 0 0-14 2.5A4.3 4.3 0 0 0 12 29z" fill="#b5a593"/></svg>',
      cloud: '<svg viewBox="0 0 36 36"><path d="M10 28h16a6 6 0 0 0 0-12 8 8 0 0 0-15.4 2.6A4.8 4.8 0 0 0 10 28z" fill="#a39584"/></svg>',
      rain: '<svg viewBox="0 0 36 36"><path d="M10 22h16a6 6 0 0 0 0-12 8 8 0 0 0-15.4 2.6A4.8 4.8 0 0 0 10 22z" fill="#a39584"/><g stroke="#5d7aa0" stroke-width="2.2" stroke-linecap="round"><path d="M13 26l-1.5 4M19 26l-1.5 4M25 26l-1.5 4"/></g></svg>',
      storm: '<svg viewBox="0 0 36 36"><path d="M10 21h16a6 6 0 0 0 0-12 8 8 0 0 0-15.4 2.6A4.8 4.8 0 0 0 10 21z" fill="#7d6f62"/><path d="M19 21l-4 7h4l-2 6 6-9h-4l2-4z" fill="#e4b93c"/></svg>',
      dust: '<svg viewBox="0 0 36 36"><g stroke="#b08a5a" stroke-width="2.6" stroke-linecap="round" fill="none"><path d="M5 12h18a3.5 3.5 0 1 0-3.5-3.5"/><path d="M5 19h24a3.5 3.5 0 1 1-3.5 3.5"/><path d="M5 26h13"/></g></svg>'
    };
    var pick = function (iconUrl, isDay) {
      var code = (iconUrl || "").split("/").pop().split("?")[0].split(",")[0];
      if (/tsra/.test(code)) return "storm";
      if (/rain|shra|fzra|snow|sleet/.test(code)) return "rain";
      if (/dust|haze|smoke|fog/.test(code)) return "dust";
      if (/ovc|bkn/.test(code)) return "cloud";
      if (/sct|few/.test(code)) return isDay ? "partly" : "cloud";
      return isDay ? "sun" : "moon";
    };
    var show = function (d) {
      document.getElementById("wx-temp").textContent = d.temp + "°F";
      document.getElementById("wx-cond").textContent = d.text;
      document.getElementById("wx-icon").innerHTML = icons[d.icon];
      wx.setAttribute("aria-label", "Phoenix weather now: " + d.temp + " degrees Fahrenheit, " + d.text);
      wx.hidden = false;
    };
    var cacheKey = "plm-wx";
    var cached = null;
    try { cached = JSON.parse(sessionStorage.getItem(cacheKey)); } catch (e) {}
    if (cached && Date.now() - cached.at < 15 * 60 * 1000) {
      show(cached);
    } else {
      fetch("https://api.weather.gov/stations/KPHX/observations/latest", { headers: { Accept: "application/geo+json" } })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (j) {
          var p = j.properties || {};
          var c = p.temperature && p.temperature.value;
          if (c === null || c === undefined) return;
          var isDay = !/\/night\//.test(p.icon || "");
          var d = { temp: Math.round(c * 9 / 5 + 32), text: p.textDescription || "", icon: pick(p.icon, isDay), at: Date.now() };
          show(d);
          try { sessionStorage.setItem(cacheKey, JSON.stringify(d)); } catch (e) {}
        })
        .catch(function () { /* leave the weather hidden if the service is unavailable */ });
    }
  }

  var y = document.getElementById("year");
  if (y) y.textContent = now.getFullYear();
})();
