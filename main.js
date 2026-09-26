/* ============================================================
   CLAUDIA SOUSA ART´S MARCLARO — main.js
   i18n (PT/EN) · header · formulários (WhatsApp/email) · lightbox
   ============================================================ */
(function () {
  'use strict';
  var WA = '351919758281';
  var EMAIL = 'claudimar60@gmail.com';

  function waHref(msg) {
    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(msg);
  }
  function cur() { return document.documentElement.lang === 'en' ? 'en' : 'pt'; }
  function T(pt, en) { return cur() === 'en' ? en : pt; }

  /* ---------------- i18n ---------------- */
  var saved = (function () {
    try { return localStorage.getItem('mcl-lang') || 'pt'; } catch (e) { return 'pt'; }
  })();

  function applyLang(lang) {
    document.documentElement.lang = lang;
    document.querySelectorAll('[data-en]').forEach(function (el) {
      el.textContent = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-pt');
    });
    document.querySelectorAll('[data-en-ph]').forEach(function (el) {
      el.placeholder = lang === 'en' ? el.getAttribute('data-en-ph') : el.getAttribute('data-pt-ph');
    });
    document.querySelectorAll('[data-en-aria]').forEach(function (el) {
      el.setAttribute('aria-label',
        lang === 'en' ? el.getAttribute('data-en-aria') : el.getAttribute('data-pt-aria'));
    });
    document.querySelectorAll('.lang-btn').forEach(function (b) {
      var on = b.dataset.lang === lang;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', String(on));
    });
  }

  /* ---------------- header ---------------- */
  function initHead() {
    var head = document.querySelector('.site-head');
    if (!head) return;
    var toggle = head.querySelector('.nav-toggle');
    if (toggle) {
      toggle.addEventListener('click', function () {
        var open = head.classList.toggle('nav-open');
        toggle.setAttribute('aria-expanded', String(open));
      });
      head.querySelectorAll('.main-nav a').forEach(function (a) {
        a.addEventListener('click', function () {
          head.classList.remove('nav-open');
          toggle.setAttribute('aria-expanded', 'false');
        });
      });
    }
    var onScroll = function () { head.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------------- filtros do portefólio ---------------- */
  function initFilters() {
    document.querySelectorAll('.filters').forEach(function (bar) {
      var grid = bar.parentElement.querySelector('.works-grid');
      if (!grid) return;
      bar.querySelectorAll('.filter-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          bar.querySelectorAll('.filter-btn').forEach(function (b) {
            b.classList.toggle('active', b === btn);
          });
          var f = btn.dataset.filter;
          grid.querySelectorAll('.work').forEach(function (w) {
            w.style.display = (f === 'all' || w.dataset.cat === f) ? '' : 'none';
          });
        });
      });
    });
  }

  /* ---------------- lightbox ---------------- */
  function initLightbox() {
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-lb-item]'));
    if (!items.length) return;
    var lb = document.createElement('div');
    lb.className = 'lb';
    lb.hidden = true;
    lb.innerHTML =
      '<button class="lb-btn lb-close" aria-label="Fechar (Esc)">&times;</button>' +
      '<button class="lb-btn lb-prev" aria-label="Anterior">&larr;</button>' +
      '<figure><img alt=""><figcaption><strong></strong><small></small></figcaption></figure>' +
      '<button class="lb-btn lb-next" aria-label="Seguinte">&rarr;</button>';
    document.body.appendChild(lb);
    var img = lb.querySelector('img'),
        strong = lb.querySelector('figcaption strong'),
        small = lb.querySelector('figcaption small'),
        idx = 0;

    function show(i) {
      idx = (i + items.length) % items.length;
      var it = items[idx];
      var pic = it.querySelector('img');
      img.src = it.getAttribute('data-lb-item');
      img.alt = pic ? pic.alt : '';
      var t = it.querySelector('figcaption strong');
      var c = it.querySelector('figcaption small');
      strong.textContent = t ? t.textContent : '';
      small.textContent = c ? c.textContent : '';
    }
    function open(i) { show(i); lb.hidden = false; document.body.style.overflow = 'hidden'; }
    function close() { lb.hidden = true; document.body.style.overflow = ''; }

    items.forEach(function (it, i) {
      it.style.cursor = 'zoom-in';
      it.addEventListener('click', function () { open(i); });
    });
    lb.querySelector('.lb-close').addEventListener('click', close);
    lb.querySelector('.lb-prev').addEventListener('click', function () { show(idx - 1); });
    lb.querySelector('.lb-next').addEventListener('click', function () { show(idx + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
    document.addEventListener('keydown', function (e) {
      if (lb.hidden) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') show(idx - 1);
      if (e.key === 'ArrowRight') show(idx + 1);
    });
  }

  /* ---------------- formulários ---------------- */
  function bindForm(form, mode) {
    if (!form) return;
    var err = form.querySelector('.form-error');
    var g = function (n) {
      var el = form.querySelector('[name="' + n + '"]');
      return el ? el.value.trim() : '';
    };
    form.addEventListener('input', function () { if (err) err.classList.remove('show'); });

    form.querySelectorAll('[data-wa-submit]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var nome = g('nome'), contacto = g('contacto');
        var tipo = mode === 'booking' ? g('tipo') : g('assunto');
        if (!nome || !contacto || !tipo) { if (err) err.classList.add('show'); return; }
        var msg, subject;
        if (mode === 'booking') {
          var data = g('data'), hora = g('hora'), pessoas = g('pessoas'), notas = g('notas');
          msg = T('Olá Claudia! Gostava de reservar:\n\nTipo: ' + tipo,
                  'Hi Claudia! I would like to book:\n\nType: ' + tipo);
          if (data) msg += '\n' + T('Data', 'Date') + ': ' + data;
          if (hora) msg += '\n' + T('Hora', 'Time') + ': ' + hora;
          if (pessoas) msg += '\n' + T('Pessoas', 'People') + ': ' + pessoas;
          msg += '\n' + T('Nome', 'Name') + ': ' + nome +
                 '\n' + T('Contacto', 'Contact') + ': ' + contacto;
          if (notas) msg += '\n' + T('Notas', 'Notes') + ': ' + notas;
          subject = 'Reserva — ' + tipo;
        } else {
          var assunto = g('assunto'), email = g('email'), mensagem = g('mensagem');
          msg = T('Olá Claudia!\n\nAssunto: ' + assunto,
                  'Hi Claudia!\n\nSubject: ' + assunto) +
                '\n' + T('Nome', 'Name') + ': ' + nome +
                '\n' + T('Email', 'Email') + ': ' + email +
                '\n\n' + mensagem;
          subject = 'Contacto — ' + assunto;
        }
        window.open(waHref(msg), '_blank', 'noopener');
        if (mode === 'contact' && !email) { /* WA não precisa de email */ }
      });
    });

    form.querySelectorAll('[data-mail-submit]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var nome = g('nome'), contacto = g('contacto');
        var tipo = mode === 'booking' ? g('tipo') : g('assunto');
        if (!nome || !contacto || !tipo) { if (err) err.classList.add('show'); return; }
        var msg, subject;
        if (mode === 'booking') {
          var data = g('data'), hora = g('hora'), pessoas = g('pessoas'), notas = g('notas');
          msg = 'Olá Claudia! Gostava de reservar:\n\nTipo: ' + tipo +
                (data ? '\nData: ' + data : '') +
                (hora ? '\nHora: ' + hora : '') +
                (pessoas ? '\nPessoas: ' + pessoas : '') +
                '\nNome: ' + nome + '\nContacto: ' + contacto +
                (notas ? '\nNotas: ' + notas : '');
          subject = 'Reserva — ' + tipo;
        } else {
          var assunto = g('assunto'), email = g('email'), mensagem = g('mensagem');
          msg = 'Olá Claudia!\n\nAssunto: ' + assunto +
                '\nNome: ' + nome + '\nEmail: ' + email + '\n\n' + mensagem;
          subject = 'Contacto — ' + assunto;
        }
        location.href = 'mailto:' + EMAIL +
          '?subject=' + encodeURIComponent(subject) +
          '&body=' + encodeURIComponent(msg);
      });
    });
  }

  /* ---------------- reveal on scroll ---------------- */
  function initReveal() {
    var els = document.querySelectorAll('.reveal');
    if (!els.length) return;
    if (!('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  }

  /* ---------------- init ---------------- */
  document.addEventListener('DOMContentLoaded', function () {
    /* capturar textos PT originais */
    document.querySelectorAll('[data-en]').forEach(function (el) {
      if (!el.hasAttribute('data-pt')) el.setAttribute('data-pt', el.textContent);
    });
    document.querySelectorAll('[data-en-ph]').forEach(function (el) {
      if (!el.hasAttribute('data-pt-ph')) el.setAttribute('data-pt-ph', el.getAttribute('placeholder') || '');
    });
    document.querySelectorAll('[data-en-aria]').forEach(function (el) {
      if (!el.hasAttribute('data-pt-aria')) el.setAttribute('data-pt-aria', el.getAttribute('aria-label') || '');
    });

    document.querySelectorAll('.lang-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        try { localStorage.setItem('mcl-lang', b.dataset.lang); } catch (e) {}
        applyLang(b.dataset.lang);
      });
    });
    applyLang(saved);

    /* links WhatsApp estáticos */
    document.querySelectorAll('[data-wa]').forEach(function (a) {
      a.href = waHref(a.getAttribute('data-wa'));
    });

    initHead();
    initFilters();
    initLightbox();
    bindForm(document.getElementById('booking-form'), 'booking');
    bindForm(document.getElementById('contact-form'), 'contact');
    initReveal();

    var y = document.getElementById('year');
    if (y) y.textContent = new Date().getFullYear();
  });
})();
