/* Contact form validation, loading state, and the sticky mobile call-to-action. */
(function () {
  'use strict';

  var form = document.getElementById('contactForm');
  var alertBox = document.getElementById('formAlert');
  var alertText = document.getElementById('formAlertText');
  var btn = document.getElementById('submitBtn');

  function errorBox(name) { return document.getElementById(name + '-error'); }

  function setError(input, message) {
    var box = errorBox(input.name);
    input.classList.add('is-invalid');
    input.setAttribute('aria-invalid', 'true');
    input.setAttribute('aria-describedby', input.name + '-error');
    if (box) { box.textContent = message; box.hidden = false; }
  }
  function clearError(input) {
    var box = errorBox(input.name);
    input.classList.remove('is-invalid');
    input.removeAttribute('aria-invalid');
    if (box) { box.textContent = ''; box.hidden = true; }
  }

  var rules = {
    name: function (v) { return v.trim().length < 2 ? 'Please tell me your name.' : ''; },
    email: function (v) {
      if (!v.trim()) return 'Please enter your email so I can reply.';
      return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? '' : "That email address doesn't look right.";
    },
    message: function (v) {
      if (!v.trim()) return 'Please write a short message.';
      return v.trim().length < 10 ? 'Please write at least a sentence (10+ characters).' : '';
    }
  };

  function showAlert(text) {
    if (!alertBox) return;
    alertText.textContent = text;
    alertBox.hidden = false;
  }

  function setLoading(on) {
    if (!btn) return;
    btn.disabled = on;
    btn.setAttribute('aria-busy', on ? 'true' : 'false');
    btn.querySelector('.btn-label').hidden = on;
    btn.querySelector('.btn-loading').hidden = !on;
  }

  if (form) {
    Object.keys(rules).forEach(function (name) {
      var input = form.elements[name];
      if (!input) return;
      input.addEventListener('blur', function () {
        if (input.value === '' && !input.classList.contains('is-invalid')) return;
        var msg = rules[name](input.value);
        msg ? setError(input, msg) : clearError(input);
      });
      input.addEventListener('input', function () {
        if (input.classList.contains('is-invalid') && !rules[name](input.value)) clearError(input);
      });
    });

    form.addEventListener('submit', function (e) {
      var firstBad = null, count = 0;
      Object.keys(rules).forEach(function (name) {
        var input = form.elements[name];
        if (!input) return;
        var msg = rules[name](input.value);
        if (msg) { setError(input, msg); count++; if (!firstBad) firstBad = input; }
        else clearError(input);
      });
      if (count) {
        e.preventDefault();
        showAlert(count === 1 ? 'Please fix the highlighted field and try again.'
                              : 'Please fix the ' + count + ' highlighted fields and try again.');
        firstBad.focus();
        return;
      }
      if (alertBox) alertBox.hidden = true;
      setLoading(true);
    });

    // Restore the button if the visitor comes back with the browser's Back button.
    window.addEventListener('pageshow', function (e) { if (e.persisted) setLoading(false); });

    // The server rejected the form: bring the visitor to the problem.
    var firstServerError = form.querySelector('.is-invalid');
    if (!firstServerError && alertBox && !alertBox.hidden) {
      setTimeout(function () { alertBox.scrollIntoView({ block: 'center' }); alertBox.focus(); }, 120);
    }
    if (firstServerError) {
      setTimeout(function () {
        if (alertBox && !alertBox.hidden) { alertBox.scrollIntoView({ block: 'center' }); alertBox.focus(); }
        else firstServerError.focus();
      }, 120);
    }
  }

  // Sticky mobile CTA: appears after the hero button scrolls away, hides over the contact form.
  var cta = document.getElementById('mobileCta');
  var heroCta = document.querySelector('.hero .btn-accent');
  var contact = document.getElementById('contact');
  if (cta && heroCta && contact && 'IntersectionObserver' in window) {
    var heroVisible = true, contactVisible = false;
    function update() { cta.classList.toggle('show', !heroVisible && !contactVisible); }
    new IntersectionObserver(function (en) { heroVisible = en[0].isIntersecting; update(); }).observe(heroCta);
    new IntersectionObserver(function (en) { contactVisible = en[0].isIntersecting; update(); },
      { threshold: 0.15 }).observe(contact);
  }
})();
