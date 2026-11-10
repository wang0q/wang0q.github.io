/*
 * Lingqing Wang — personal website
 * Mobile menu, nav state, active-section highlighting, scroll reveal, citation copy.
 */
(function () {
  "use strict";

  var nav = document.querySelector(".site-nav");
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");

  /* Mobile menu */
  function setMenu(open) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("no-scroll", open);
  }

  if (toggle && links) {
    toggle.addEventListener("click", function () {
      setMenu(!nav.classList.contains("is-open"));
    });
    links.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setMenu(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        setMenu(false);
        toggle.focus();
      }
    });
    window.matchMedia("(min-width: 821px)").addEventListener("change", function (mq) {
      if (mq.matches) setMenu(false);
    });
  }

  /* Hairline under the nav once the page scrolls */
  function onScroll() {
    if (nav) nav.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  var hasIO = "IntersectionObserver" in window;

  /* Highlight the nav link for the section in view (home page only) */
  var sectionLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
  if (hasIO && sectionLinks.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        sectionLinks.forEach(function (a) {
          a.classList.toggle("is-active", a.getAttribute("href") === "#" + entry.target.id);
        });
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    sectionLinks.forEach(function (a) {
      var section = document.querySelector(a.getAttribute("href"));
      if (section) spy.observe(section);
    });
  }

  /* Fade sections in as they enter the viewport */
  var revealables = document.querySelectorAll("[data-reveal]");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (hasIO && !reduceMotion) {
    var reveal = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        reveal.unobserve(entry.target);
      });
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });
    revealables.forEach(function (el) { reveal.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Copy-citation buttons on project pages */
  document.querySelectorAll("[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      var source = document.getElementById(button.getAttribute("data-copy"));
      if (!source) return;
      var text = source.textContent.replace(/\s+/g, " ").trim();
      var done = function (label) {
        button.textContent = label;
        setTimeout(function () { button.textContent = "Copy"; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { done("Copied"); }, function () { done("Press ⌘C"); });
      } else {
        var range = document.createRange();
        range.selectNodeContents(source);
        var sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        done("Press ⌘C");
      }
    });
  });

  /* Scrollable news: fade whichever edge has more items beyond it */
  function watchNewsScroll(box) {
    function update() {
      var max = box.scrollHeight - box.clientHeight;
      box.classList.toggle("can-scroll-up", box.scrollTop > 2);
      box.classList.toggle("can-scroll-down", box.scrollTop < max - 2);
    }
    box.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
    return update;
  }

  /* The home page's news window loads its items from news.html,
     so news only has to be written in one place. */
  document.querySelectorAll(".news-scroll").forEach(function (box) {
    var update = watchNewsScroll(box);
    var src = box.getAttribute("data-news-src");
    if (!src || !window.fetch || !window.DOMParser) return;
    fetch(src).then(function (res) {
      if (!res.ok) throw new Error("HTTP " + res.status);
      return res.text();
    }).then(function (html) {
      var list = new DOMParser().parseFromString(html, "text/html").querySelector(".news-list");
      if (!list) return;
      list.removeAttribute("data-reveal");
      box.replaceChildren(document.importNode(list, true));
      update();
    }).catch(function () { /* keep the "See the latest news" link */ });
  });

  /* Current year in the footer */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
