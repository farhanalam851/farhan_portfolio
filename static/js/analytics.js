/* Cookie consent + Google Analytics 4 (loaded only after the visitor accepts). */
(function () {
  'use strict';

  var KEY = 'cookie-consent';
  var gaId = window.GA_ID || '';
  var banner = document.getElementById('cookieBanner');
  var acceptBtn = document.getElementById('cookieAccept');
  var declineBtn = document.getElementById('cookieDecline');
  var settingsBtn = document.getElementById('cookieSettings');

  function getConsent() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function setConsent(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }

  function clearGaCookies() {
    var host = location.hostname;
    var parts = host.split('.');
    var domains = [host, '.' + host, '.' + parts.slice(-2).join('.')];
    document.cookie.split(';').forEach(function (c) {
      var name = c.split('=')[0].trim();
      if (name === '_ga' || name.indexOf('_ga_') === 0) {
        var expired = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
        document.cookie = expired;
        domains.forEach(function (d) { document.cookie = expired + '; domain=' + d; });
      }
    });
  }

  function loadAnalytics() {
    if (!gaId || window.__gaLoaded) return;
    window.__gaLoaded = true;
    window['ga-disable-' + gaId] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', gaId);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(gaId);
    document.head.appendChild(s);

    // A page can ask for one conversion event on load (the thank-you page after a real enquiry).
    var pageEvent = document.body.getAttribute('data-page-event');
    if (pageEvent) window.track(pageEvent, { form: 'contact' });
  }

  function disableAnalytics() {
    if (gaId) window['ga-disable-' + gaId] = true;
    clearGaCookies();
  }

  // Safe to call anywhere; does nothing unless analytics is configured and accepted.
  window.track = function (name, params) {
    if (window.gtag && getConsent() === 'granted') window.gtag('event', name, params || {});
  };

  function showBanner() {
    if (!banner) return;
    banner.hidden = false;
    document.body.classList.add('banner-open');
  }
  function hideBanner() {
    if (!banner) return;
    banner.hidden = true;
    document.body.classList.remove('banner-open');
  }

  if (acceptBtn) acceptBtn.addEventListener('click', function () {
    setConsent('granted'); hideBanner(); loadAnalytics();
  });
  if (declineBtn) declineBtn.addEventListener('click', function () {
    setConsent('denied'); hideBanner(); disableAnalytics();
  });
  if (settingsBtn) settingsBtn.addEventListener('click', function () {
    showBanner();
    if (acceptBtn) acceptBtn.focus();
  });

  var consent = getConsent();
  if (consent === 'granted') loadAnalytics();
  else if (consent === null) setTimeout(showBanner, 800);

  // Click tracking for any element with data-track="event_name"
  document.addEventListener('click', function (e) {
    var el = e.target.closest ? e.target.closest('[data-track]') : null;
    if (el) window.track(el.getAttribute('data-track'), { page: location.pathname });
  });
})();
