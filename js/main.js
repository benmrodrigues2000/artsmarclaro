/* Marclaro — site behaviour (no dependencies) */
(function () {
  const WA = "351919758281";
  const EMAIL = "claudimar60@gmail.com";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  let lang = localStorage.getItem("mc-lang") === "en" ? "en" : "pt";
  const t = (pt, en) => (lang === "en" ? en : pt);

  /* ---------- Language ---------- */
  function applyLang() {
    document.documentElement.lang = lang === "en" ? "en" : "pt-PT";
    $$("[data-en]").forEach((el) => {
      if (el.dataset.pt === undefined) el.dataset.pt = el.innerHTML;
      el.innerHTML = lang === "en" ? el.dataset.en : el.dataset.pt;
    });
    $$("[data-en-ph]").forEach((el) => {
      if (el.dataset.ptPh === undefined) el.dataset.ptPh = el.placeholder;
      el.placeholder = lang === "en" ? el.dataset.enPh : el.dataset.ptPh;
    });
    $$("[data-en-alt]").forEach((el) => {
      if (el.dataset.ptAlt === undefined) el.dataset.ptAlt = el.alt;
      el.alt = lang === "en" ? el.dataset.enAlt : el.dataset.ptAlt;
    });
    const md = $('meta[name="description"]');
    if (md && md.dataset.en) {
      if (!md.dataset.pt) md.dataset.pt = md.content;
      md.content = lang === "en" ? md.dataset.en : md.dataset.pt;
    }
    $$(".lang button").forEach((b) => b.setAttribute("aria-pressed", b.dataset.lang === lang));
    updateWA();
    renderCart();
  }
  $$(".lang button").forEach((b) =>
    b.addEventListener("click", () => {
      lang = b.dataset.lang;
      localStorage.setItem("mc-lang", lang);
      applyLang();
    })
  );

  /* ---------- WhatsApp links (pre-filled) ---------- */
  function waLink(msg) {
    return `https://wa.me/${WA}?text=${encodeURIComponent(msg)}`;
  }
  function updateWA() {
    $$("[data-wa]").forEach((a) => {
      const msg = lang === "en" && a.dataset.waEn ? a.dataset.waEn : a.dataset.wa;
      a.href = waLink(msg);
      a.target = "_blank";
      a.rel = "noopener";
    });
  }

  /* ---------- Mobile nav ---------- */
  const burger = $(".burger"), nav = $(".nav");
  const setNav = (open) => { burger.setAttribute("aria-expanded", open); nav.classList.toggle("open", open); };
  if (burger) {
    burger.addEventListener("click", () => setNav(burger.getAttribute("aria-expanded") !== "true"));
    nav.addEventListener("click", (e) => { if (e.target.closest("a")) setNav(false); });
  }

  /* ---------- Reveal on scroll ---------- */
  const io = "IntersectionObserver" in window ? new IntersectionObserver((es) => {
    es.forEach((e) => { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
  }, { rootMargin: "0px 0px -8% 0px" }) : null;
  $$(".rv").forEach((el) => (io ? io.observe(el) : el.classList.add("in")));

  /* ---------- Home work rail ---------- */
  const rail = $(".rail");
  if (rail) {
    const bar = $(".rail-line span");
    const upd = () => {
      const max = rail.scrollWidth - rail.clientWidth;
      const vis = rail.clientWidth / rail.scrollWidth;
      bar.style.width = Math.max(12, vis * 100) + "%";
      bar.style.left = (max > 0 ? (rail.scrollLeft / max) * (100 - Math.max(12, vis * 100)) : 0) + "%";
    };
    rail.addEventListener("scroll", upd, { passive: true });
    window.addEventListener("resize", upd);
    upd();
    $$(".rail-btn").forEach((b) => b.addEventListener("click", () => {
      const card = $(".arch-card", rail);
      rail.scrollBy({ left: (+b.dataset.dir) * (card.offsetWidth + 22), behavior: "smooth" });
    }));
  }

  /* ---------- Portfolio filters + lightbox ---------- */
  const filters = $$(".filters button");
  filters.forEach((b) => b.addEventListener("click", () => {
    filters.forEach((x) => x.setAttribute("aria-pressed", x === b));
    const f = b.dataset.filter;
    $$(".masonry .item").forEach((it) => it.classList.toggle("hide", f !== "all" && !it.dataset.cat.split(" ").includes(f)));
  }));

  const lb = $(".lb");
  if (lb) {
    let idx = 0;
    const visible = () => $$(".masonry .item:not(.hide)");
    const show = (i) => {
      const v = visible(); idx = (i + v.length) % v.length;
      const img = $("img", v[idx]);
      $("img", lb).src = img.src; $("img", lb).alt = img.alt;
      $("p", lb).textContent = img.alt;
    };
    $$(".masonry .item").forEach((it) => it.addEventListener("click", () => {
      show(visible().indexOf(it)); lb.classList.add("open"); document.body.style.overflow = "hidden"; $(".x", lb).focus();
    }));
    const close = () => { lb.classList.remove("open"); document.body.style.overflow = ""; };
    $(".x", lb).onclick = close;
    $(".prev", lb).onclick = () => show(idx - 1);
    $(".next", lb).onclick = () => show(idx + 1);
    lb.addEventListener("click", (e) => { if (e.target === lb) close(); });
    document.addEventListener("keydown", (e) => {
      if (!lb.classList.contains("open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "ArrowRight") show(idx + 1);
    });
    let x0 = null;
    lb.addEventListener("touchstart", (e) => (x0 = e.touches[0].clientX), { passive: true });
    lb.addEventListener("touchend", (e) => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; if (Math.abs(dx) > 50) show(idx + (dx < 0 ? 1 : -1)); x0 = null; });
  }

  /* ---------- Shop / cart (the drawer is in the footer of every page) ---------- */
  let cart = [];
  try { cart = JSON.parse(localStorage.getItem("mc-cart") || "[]"); if (!Array.isArray(cart)) cart = []; }
  catch { cart = []; }
  const eur = (n) => n.toLocaleString("pt-PT", { style: "currency", currency: "EUR" });
  const save = () => localStorage.setItem("mc-cart", JSON.stringify(cart));
  const drawer = $("#cart"), veil = $(".veil");
  let cartOpen = false, cartTrigger = null;

  function renderCart(added) {
    const n = cart.reduce((s, i) => s + i.q, 0);
    $$(".cart-count").forEach((c) => {
      const was = +c.dataset.n || 0;
      c.textContent = n || ""; c.dataset.n = n;
      if (added && n > was) { c.classList.remove("pop"); void c.offsetWidth; c.classList.add("pop"); }
    });
    const box = $(".drawer .items");
    if (!box) return;
    if (!cart.length) {
      box.innerHTML = `<p class="empty">${t("O seu carrinho está vazio.", "Your cart is empty.")}<small>${t("Espreite a loja e junte as suas peças favoritas.", "Have a look at the shop and add your favourite pieces.")}</small></p>`;
    } else {
      box.innerHTML = cart.map((i, k) => `<div class="ci"><img src="${i.img}" alt=""><div><b>${lang === "en" ? i.en : i.pt}</b><small>${i.q} × ${eur(i.p)}</small></div><button type="button" data-rm="${k}">${t("remover", "remove")}</button></div>`).join("");
    }
    const tot = $(".drawer .total b"), co = $(".drawer .checkout");
    if (tot) tot.textContent = eur(cart.reduce((s, i) => s + i.q * i.p, 0));
    if (co) { co.toggleAttribute("disabled", !cart.length); co.style.opacity = cart.length ? 1 : .5; }
  }

  function openCart(o) {
    if (!drawer || cartOpen === o) return;
    if (o) cartTrigger = document.activeElement;
    cartOpen = o;
    const setInert = (el, on) => { if (el) on ? el.setAttribute("inert", "") : el.removeAttribute("inert"); };
    setInert(drawer, !o);
    // while open, the rest of the page goes inert too (the veil stays clickable: it closes the cart)
    $$("body > *").forEach((el) => { if (el !== drawer && el !== veil) setInert(el, o); });
    drawer.classList.toggle("open", o);
    if (veil) veil.classList.toggle("open", o);
    drawer.setAttribute("aria-hidden", o ? "false" : "true");
    document.body.classList.toggle("locked", o);
    $$(".cart-btn").forEach((b) => b.setAttribute("aria-expanded", o ? "true" : "false"));
    if (o) { const x = $("[data-cart-close]", drawer); if (x) x.focus(); }
    else {
      const back = cartTrigger && cartTrigger !== document.body && document.contains(cartTrigger) ? cartTrigger : $(".cart-btn");
      if (back) back.focus();
      cartTrigger = null;
    }
  }
  // the cart icon in the header (and in the mobile bar) opens the drawer on any page
  $$(".cart-btn").forEach((b) => b.addEventListener("click", (e) => {
    if (!drawer) { const h = b.getAttribute("href"); if (h) location.href = h; return; } // no drawer: fall back to the shop
    e.preventDefault(); openCart(true);
  }));
  if (drawer) {
    // ×, the veil and "keep shopping" all close it
    document.addEventListener("click", (e) => {
      const c = e.target.closest("[data-cart-close]");
      if (!c) return;
      e.preventDefault(); openCart(false);
    });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && cartOpen) openCart(false); });
    drawer.addEventListener("click", (e) => {
      const rm = e.target.closest("[data-rm]");
      if (rm) { cart.splice(+rm.dataset.rm, 1); save(); renderCart(); }
    });
    const co = $(".drawer .checkout");
    if (co) co.onclick = () => {
      if (!cart.length) return;
      const lines = cart.map((i) => `• ${i.q} × ${lang === "en" ? i.en : i.pt} (${eur(i.p)})`).join("\n");
      const tot = eur(cart.reduce((s, i) => s + i.q * i.p, 0));
      const msg = t(`Olá Claudia! Gostava de encomendar:\n${lines}\nTotal: ${tot}\n\nNome:\nMorada de entrega (ou levantamento no ateliê):`,
                    `Hi Claudia! I'd like to order:\n${lines}\nTotal: ${tot}\n\nName:\nDelivery address (or pick-up at the studio):`);
      window.open(waLink(msg), "_blank", "noopener");
    };
  }
  $$(".prod").forEach((p) => {
    const inp = $(".qty input", p);
    $$(".qty button", p).forEach((b) => b.onclick = () => { inp.value = Math.max(1, Math.min(20, (+inp.value || 1) + (+b.dataset.d))); });
    $(".add", p).onclick = () => {
      const d = p.dataset, q = Math.max(1, +inp.value || 1);
      const ex = cart.find((i) => i.id === d.id);
      ex ? (ex.q += q) : cart.push({ id: d.id, pt: d.npt, en: d.nen, p: +d.price, img: $("img", p).getAttribute("src"), q });
      save(); renderCart(true); inp.value = 1; openCart(true);
    };
  });

  /* ---------- Forms (contact + booking) ---------- */
  $$("form[data-kind]").forEach((f) => {
    f.addEventListener("submit", async (e) => {
      e.preventDefault();
      let ok = true;
      $$("[required]", f).forEach((el) => {
        const fld = el.closest(".field") || el.closest(".check");
        let valid = el.type === "checkbox" ? el.checked : el.value.trim() !== "";
        if (valid && el.type === "email") valid = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(el.value.trim());
        if (valid && el.type === "tel" && el.value) valid = /^[+\d\s()-]{9,}$/.test(el.value.trim());
        if (fld) fld.classList.toggle("invalid", !valid);
        if (!valid) ok = false;
      });
      if (!ok) { const first = $(".invalid input, .invalid select, .invalid textarea", f); if (first) first.focus(); return; }

      const endpoint = f.dataset.endpoint; // e.g. https://formspree.io/f/xxxx — see GUIA.md
      const okBox = $(".ok", f);
      if (endpoint) {
        try {
          const r = await fetch(endpoint, { method: "POST", headers: { Accept: "application/json" }, body: new FormData(f) });
          if (!r.ok) throw 0;
        } catch { alert(t("Não foi possível enviar. Por favor tente pelo WhatsApp.", "Could not send. Please try WhatsApp.")); return; }
      } else {
        // No backend yet: open WhatsApp with the full request (the fastest reply channel)
        const body = [...f.elements]
          .filter((el) => el.name && el.name !== "rgpd" && el.type !== "checkbox")
          .map((el) => {
            const lab = el.id && f.querySelector(`label[for="${el.id}"]`);
            const name = lab ? lab.textContent.replace("*", "").trim() : el.name;
            let val = el.tagName === "SELECT" ? el.selectedOptions[0].textContent.trim() : el.value.trim();
            if (el.type === "date" && el.value) val = new Date(el.value + "T00:00").toLocaleDateString(lang === "en" ? "en-GB" : "pt-PT");
            return val ? `${name}: ${val}` : null;
          })
          .filter(Boolean).join("\n");
        const head = f.dataset.kind === "booking" ? t("Pedido de marcação", "Booking request") : t("Mensagem do site", "Website message");
        window.open(waLink(`${head}\n\n${body}`), "_blank", "noopener");
      }
      okBox.classList.add("show");
      f.reset();
      okBox.scrollIntoView({ behavior: "smooth", block: "center" });
    });
    $$("input,select,textarea", f).forEach((el) => el.addEventListener("input", () => (el.closest(".field") || el.closest(".check") || {}).classList?.remove("invalid")));
  });
  // pre-select subject / service via ?assunto=… or ?servico=…
  const qs = new URLSearchParams(location.search);
  ["assunto", "servico"].forEach((k) => { const v = qs.get(k), el = document.getElementsByName(k)[0]; if (v && el) el.value = v; });

  /* ---------- Newsletter ---------- */
  $$(".news").forEach((n) => n.addEventListener("submit", (e) => {
    e.preventDefault();
    const em = $("input", n).value.trim();
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(em)) { $("input", n).focus(); return; }
    location.href = `mailto:${EMAIL}?subject=${encodeURIComponent("Newsletter")}&body=${encodeURIComponent(t("Quero receber novidades: ", "Please add me: ") + em)}`;
    $("input", n).value = ""; $("input", n).placeholder = t("Obrigada!", "Thank you!");
  }));

  /* ---------- Cookie notice (GDPR) + analytics only after consent ---------- */
  const ck = $(".cookie"), consent = localStorage.getItem("mc-consent");
  function loadAnalytics() {
    // Plausible (privacy-friendly). Replace data-domain once the domain is live.
    const s = document.createElement("script");
    s.defer = true; s.dataset.domain = "marclaroarts.pt"; s.src = "https://plausible.io/js/script.js";
    document.head.appendChild(s);
  }
  if (ck) {
    if (!consent) setTimeout(() => ck.classList.add("show"), 900);
    else if (consent === "yes") loadAnalytics();
    $$(".cookie [data-c]").forEach((b) => b.onclick = () => {
      localStorage.setItem("mc-consent", b.dataset.c); ck.classList.remove("show");
      if (b.dataset.c === "yes") loadAnalytics();
    });
  }

  $$(".year").forEach((y) => (y.textContent = new Date().getFullYear()));
  applyLang();
})();
