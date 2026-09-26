/* Marclaro — site behaviour (no dependencies) */
(function () {
  const WA = "351919758281";
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  // A blocked or unavailable browser store must not break navigation or forms.
  const storage = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); } catch { /* session only */ } },
    remove(key) { try { localStorage.removeItem(key); } catch { /* already unavailable */ } }
  };
  storage.remove("mc-consent"); // Retire the old analytics choice; no analytics are loaded.
  let lang = storage.get("mc-lang") === "en" ? "en" : "pt";
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
      storage.set("mc-lang", lang);
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

  function trapDialog(event, dialog) {
    if (event.key !== "Tab") return;
    const focusable = [...dialog.querySelectorAll('a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex="0"]')].filter(el => el.getClientRects().length && !el.closest('[hidden]'));
    const first = focusable[0], last = focusable[focusable.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
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
    let idx = 0, lightboxTrigger = null;
    lb.addEventListener("keydown", (e) => trapDialog(e, lb));
    const visible = () => $$(".masonry .item:not(.hide)");
    const show = (i) => {
      const v = visible(); idx = (i + v.length) % v.length;
      const img = $("img", v[idx]);
      $("img", lb).src = img.src; $("img", lb).alt = img.alt;
      $("p", lb).textContent = img.alt;
    };
    $$(".masonry .item").forEach((it) => it.addEventListener("click", () => {
      lightboxTrigger = it;
      show(visible().indexOf(it)); lb.classList.add("open"); document.body.style.overflow = "hidden";
      // The lightbox lives inside main; make its siblings and the surrounding UI inert.
      [...document.body.children, ...$("main").children].forEach((el) => {
        if (el !== lb && el.tagName !== "MAIN" && !el.hasAttribute("inert")) {
          el.setAttribute("inert", ""); el.dataset.lightboxInert = "";
        }
      });
      $(".x", lb).focus();
    }));
    const close = () => {
      lb.classList.remove("open"); document.body.style.overflow = "";
      $$("[data-lightbox-inert]").forEach((el) => { el.removeAttribute("inert"); delete el.dataset.lightboxInert; });
      lightboxTrigger?.focus();
    };
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
  try { cart = JSON.parse(storage.get("mc-cart") || "[]"); if (!Array.isArray(cart)) cart = []; }
  catch { cart = []; }
  cart = cart.filter((i) => i && typeof i.id === "string" && typeof i.pt === "string" &&
    typeof i.en === "string" && typeof i.img === "string" && /^img\/[a-z0-9-]+\.jpg$/.test(i.img) &&
    Number.isFinite(i.p) && i.p >= 0 && Number.isInteger(i.q) && i.q > 0 && i.q <= 20);
  const html = (value) => String(value).replace(/[&<>"']/g, (c) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  }[c]));
  const eur = (n) => n.toLocaleString("pt-PT", { style: "currency", currency: "EUR" });
  const save = () => storage.set("mc-cart", JSON.stringify(cart));
  const drawer = $("#cart"), veil = $(".veil");
  const checkoutForm = $("#checkout-form");
  let cartOpen = false, cartTrigger = null;

  function checkoutStep(show, focus = false) {
    if (!checkoutForm) return;
    checkoutForm.hidden = !show;
    $(".items", drawer).hidden = show;
    $("footer", drawer).hidden = show;
    $(".checkout", drawer).setAttribute("aria-expanded", String(show));
    if (focus) (show ? $("#checkout-name") : $(".checkout", drawer)).focus();
  }

  function clearCheckoutStatus() {
    if (!checkoutForm) return;
    $("[data-checkout-status]", checkoutForm).hidden = true;
    $("[data-checkout-link]", checkoutForm).removeAttribute("href");
  }

  function renderCart(added) {
    clearCheckoutStatus();
    const n = cart.reduce((s, i) => s + i.q, 0);
    $$(".cart-count").forEach((c) => {
      const was = +c.dataset.n || 0;
      c.textContent = n || ""; c.dataset.n = n;
      if (added && n > was) { c.classList.remove("pop"); void c.offsetWidth; c.classList.add("pop"); }
    });
    const box = $(".drawer .items");
    if (!box) return;
    if (!cart.length) {
      checkoutStep(false);
      if (checkoutForm) {
        checkoutForm.reset();
        $("#checkout-address").disabled = false;
        $("#checkout-address").required = true;
        $("[data-checkout-address]").hidden = false;
      }
      box.innerHTML = `<p class="empty">${t("O seu carrinho está vazio.", "Your cart is empty.")}<small>${t("Espreite o catálogo e junte as suas peças favoritas.", "Have a look at the catalogue and add your favourite pieces.")}</small></p>`;
    } else {
      box.innerHTML = cart.map((i, k) => `<div class="ci"><img src="${i.img}" alt=""><div><b>${html(lang === "en" ? i.en : i.pt)}</b><small>${i.q} × ${eur(i.p)}</small></div><button type="button" data-rm="${k}">${t("remover", "remove")}</button></div>`).join("");
    }
    const tot = $(".drawer .total b"), co = $(".drawer .checkout");
    if (tot) tot.textContent = eur(cart.reduce((s, i) => s + i.q * i.p, 0));
    if (co) { co.toggleAttribute("disabled", !cart.length); co.style.opacity = cart.length ? 1 : .5; }
  }

  function openCart(o) {
    if (!drawer || cartOpen === o) return;
    if (o) cartTrigger = document.activeElement;
    cartOpen = o;
    if (!o) checkoutStep(false);
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
    drawer.addEventListener("keydown", (e) => trapDialog(e, drawer));
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
      if (cart.length) checkoutStep(true, true);
    };
    if (checkoutForm) {
      $("[data-checkout-back]", checkoutForm).onclick = () => checkoutStep(false, true);
      const delivery = $("#checkout-delivery"), address = $("#checkout-address");
      delivery.addEventListener("change", () => {
        const shipping = delivery.value === "shipping";
        $("[data-checkout-address]", checkoutForm).hidden = !shipping;
        address.disabled = !shipping;
        address.required = shipping;
        address.setCustomValidity("");
        clearCheckoutStatus();
      });
      checkoutForm.addEventListener("input", (e) => {
        e.target.setCustomValidity?.("");
        clearCheckoutStatus();
      });
      checkoutForm.addEventListener("submit", (e) => {
        e.preventDefault();
        if (!cart.length) return;
        // Native validation handles email/required fields; also reject whitespace-only text.
        $$("[required]", checkoutForm).forEach((el) => {
          if (!el.disabled && el.type !== "checkbox") {
            el.setCustomValidity(el.value.trim() ? "" : t("Preencha este campo.", "Please fill in this field."));
          }
        });
        if (!checkoutForm.reportValidity()) return;
        const values = new FormData(checkoutForm);
        const value = (key) => String(values.get(key) || "").trim();
        const lines = cart.map((i) => `• ${i.q} × ${lang === "en" ? i.en : i.pt} (${eur(i.p)})`).join("\n");
        const tot = eur(cart.reduce((s, i) => s + i.q * i.p, 0));
        const details = [
          `${t("Nome", "Name")}: ${value("name")}`,
          `Email: ${value("email")}`,
          `${t("Telefone", "Phone")}: ${value("phone")}`,
          `${t("Entrega", "Delivery")}: ${delivery.selectedOptions[0].textContent}`,
          delivery.value === "shipping" ? `${t("Morada", "Address")}: ${value("address")}` : "",
          value("notes") ? `${t("Observações", "Notes")}: ${value("notes")}` : ""
        ].filter(Boolean).join("\n");
        const msg = `${t("Olá Claudia! Gostava de encomendar:", "Hi Claudia! I'd like to order:")}\n${lines}\nTotal: ${tot}\n${t("Portes a confirmar.", "Shipping to be confirmed.")}\n\n${details}`;
        const url = waLink(msg);
        $("[data-checkout-link]", checkoutForm).href = url;
        $("[data-checkout-status]", checkoutForm).hidden = false;
        window.open(url, "_blank", "noopener");
        $("[data-checkout-status]", checkoutForm).scrollIntoView({ block: "nearest" });
      });
    }
  }
  $$(".prod").forEach((p) => {
    const inp = $(".qty input", p);
    $$(".qty button", p).forEach((b) => b.onclick = () => { inp.value = Math.max(1, Math.min(20, (+inp.value || 1) + (+b.dataset.d))); });
    $(".add", p).onclick = () => {
      const d = p.dataset, q = Math.max(1, Math.min(20, Math.floor(+inp.value || 1)));
      const ex = cart.find((i) => i.id === d.id);
      ex ? (ex.q = Math.min(20, ex.q + q)) : cart.push({ id: d.id, pt: d.npt, en: d.nen, p: +d.price, img: $("img", p).getAttribute("src"), q });
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

  /* ---------- Local storage controls (no analytics or optional cookies) ---------- */
  const clearStorage = $("[data-clear-storage]");
  if (clearStorage) clearStorage.addEventListener("click", () => {
    ["mc-lang", "mc-cart", "mc-consent"].forEach((key) => storage.remove(key));
    cart = []; renderCart();
    const status = $("[data-storage-status]");
    status.dataset.pt = "O idioma guardado foi apagado e o carrinho está vazio. O idioma desta página mantém-se até sair.";
    status.dataset.en = "Your saved language was cleared and the cart is empty. This page keeps its language until you leave.";
    status.textContent = t(status.dataset.pt, status.dataset.en);
  });

  $$(".year").forEach((y) => (y.textContent = new Date().getFullYear()));
  applyLang();
})();
