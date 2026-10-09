(function () {
  'use strict';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Theme toggle
  var root = document.documentElement;
  var toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }

  // Nav shadow + scroll progress
  var nav = document.getElementById('siteNav');
  var bar = document.getElementById('scrollProgress');
  function onScroll() {
    var y = window.scrollY || document.documentElement.scrollTop;
    var h = document.documentElement.scrollHeight - window.innerHeight;
    if (nav) nav.classList.toggle('scrolled', y > 20);
    if (bar) bar.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Close mobile menu after tapping a link; scrollspy
  document.querySelectorAll('#navMenu .nav-link, #navMenu .btn').forEach(function (a) {
    a.addEventListener('click', function () {
      var m = document.getElementById('navMenu');
      if (m && m.classList.contains('show') && window.bootstrap) {
        window.bootstrap.Collapse.getOrCreateInstance(m).hide();
      }
    });
  });
  var links = document.querySelectorAll('.site-nav .nav-link');
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        links.forEach(function (l) { l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id); });
      }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  document.querySelectorAll('section[id]').forEach(function (s) { spy.observe(s); });

  // Reveal on scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('in'); });
  }

  // Count-up numbers
  function countUp(el) {
    var target = parseInt(el.getAttribute('data-count'), 10) || 0;
    if (reduce) { el.textContent = target; return; }
    var start = null, dur = 1200;
    function step(t) {
      if (!start) start = t;
      var p = Math.min((t - start) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  var counters = document.querySelectorAll('[data-count]');
  var co = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { countUp(e.target); co.unobserve(e.target); } });
  }, { threshold: 0.6 });
  counters.forEach(function (c) { co.observe(c); });

  // Typed role text
  var typedEl = document.getElementById('typed');
  var rolesEl = document.getElementById('roles-data');
  if (typedEl && rolesEl) {
    var words = JSON.parse(rolesEl.textContent);
    if (reduce) { typedEl.textContent = words[0]; }
    else {
      var w = 0, c = 0, del = false;
      (function tick() {
        var word = words[w];
        typedEl.textContent = word.slice(0, c);
        var delay = del ? 35 : 75;
        if (!del && c === word.length) { del = true; delay = 1600; }
        else if (del && c === 0) { del = false; w = (w + 1) % words.length; delay = 350; }
        else { c += del ? -1 : 1; }
        setTimeout(tick, delay);
      })();
    }
  }

  // Skill card tilt + cursor glow (fine pointers only)
  if (!reduce && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.querySelectorAll('[data-tilt]').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var r = card.getBoundingClientRect();
        var x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        card.style.transform = 'perspective(800px) rotateX(' + ((0.5 - y) * 8) + 'deg) rotateY(' + ((x - 0.5) * 10) + 'deg) translateY(-4px)';
        card.style.setProperty('--mx', (x * 100) + '%');
        card.style.setProperty('--my', (y * 100) + '%');
      });
      card.addEventListener('mouseleave', function () { card.style.transform = ''; });
    });
  }
})();
