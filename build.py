#!/usr/bin/env python3
"""Generates the Marclaro static site (HTML pages) from shared templates.
Edit text here, then run:  python3 build.py
"""
from html import escape
from legal_content import LEGAL_PAGES

SITE = "https://marclaroarts.pt"
WA_NUM = "351919758281"
EMAIL = "claudimar60@gmail.com"
PHONE = "+351 919 758 281"
IG = "https://www.instagram.com/marclaroarts/"
FB = "https://www.facebook.com/marclaro.arts"
TT = "https://www.tiktok.com/@claudimar76"


def T(pt, en, tag="span", cls="", attrs=""):
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c}{(" " + attrs) if attrs else ""} data-en="{escape(en, quote=True)}">{pt}</{tag}>'


def IMG(src, pt, en, cls="", lazy=True, extra=""):
    c = f' class="{cls}"' if cls else ""
    ld = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return f'<img src="img/{src}" alt="{escape(pt)}" data-en-alt="{escape(en)}"{c}{ld}{extra}>'


def WA(pt_label, en_label, msg_pt, msg_en, cls="btn btn-solid", icon=True):
    ic = ICON["wa"] if icon else ""
    return (f'<a class="{cls}" href="https://wa.me/{WA_NUM}" data-wa="{escape(msg_pt)}" data-wa-en="{escape(msg_en)}">'
            f'{ic}{T(pt_label, en_label)}</a>')


def CART_BTN(cls=""):
    """Header cart icon. It is a button (not a link): js/main.js opens the drawer
    that every page carries, so the cart works from any page."""
    c = f" {cls}" if cls else ""
    return (f'<button class="cart-btn{c}" type="button" aria-controls="cart" aria-expanded="false" '
            f'aria-label="Carrinho / Cart">{ICON["cart"]}<span class="cart-count"></span></button>')


def cart_drawer(on_shop=False):
    """Slide-in cart panel. Printed on every page (by foot()), so clicking the cart
    icon opens it wherever the visitor is. `on_shop` swaps the "go to the shop" link
    for a "keep shopping" button, since the products are already on screen."""
    more = (f'<button class="btn btn-line btn-sm" type="button" data-cart-close>{T("Continuar a comprar", "Keep shopping")}</button>'
            if on_shop else
            f'<a class="btn btn-line btn-sm" href="loja.html">{T("Ver o catálogo", "Browse the catalogue")}</a>')
    return f'''
<div class="veil" data-cart-close></div>
<aside class="drawer" id="cart" role="dialog" aria-modal="true" aria-label="Carrinho / Cart" aria-hidden="true" inert>
  <header>{T("O seu carrinho", "Your cart", "h3")}<button type="button" data-cart-close aria-label="Fechar / Close">×</button></header>
  <div class="items"></div>
  <footer><div class="total">{T("Total", "Total")}<b>0,00 €</b></div><small class="muted">{T("Portes calculados na confirmação.", "Shipping calculated on confirmation.")}</small>
  <button class="btn btn-solid checkout" type="button" aria-controls="checkout-form" aria-expanded="false" disabled>{T("Finalizar pedido", "Checkout")}</button>
  <p class="cart-terms">{T('O envio da mensagem é um pedido, não uma compra concluída. Consulte os <a href="termos.html">termos</a> e as <a href="envios-devolucoes.html">condições de envio e devolução</a>.', 'Sending the message is a request, not a completed purchase. Read the <a href="termos.html">terms</a> and <a href="envios-devolucoes.html">shipping and returns policy</a>.')}</p>
  {more}</footer>
  <form id="checkout-form" class="checkout-form" hidden aria-labelledby="checkout-title">
    <button class="btn btn-line btn-sm" type="button" data-checkout-back>{T("Voltar ao carrinho", "Back to cart")}</button>
    {T("Dados do pedido", "Order details", "h3", attrs='id="checkout-title"')}
    {T("Preencha os campos obrigatórios (*) antes de continuar para o WhatsApp. O pedido só é enviado quando confirmar a mensagem no WhatsApp.", "Fill in the required fields (*) before continuing to WhatsApp. Your request is only sent when you send the message in WhatsApp.", "p", "form-note")}
    <div class="field"><label for="checkout-name">{T("Nome completo *", "Full name *")}</label><input id="checkout-name" name="name" autocomplete="name" maxlength="120" pattern=".*\\S.*" required></div>
    <div class="field"><label for="checkout-email">{T("Email *", "Email *")}</label><input id="checkout-email" name="email" type="email" autocomplete="email" maxlength="160" required></div>
    <div class="field"><label for="checkout-phone">{T("Telefone *", "Phone *")}</label><input id="checkout-phone" name="phone" type="tel" autocomplete="tel" maxlength="40" pattern=".*\\S.*" required></div>
    <div class="field"><label for="checkout-delivery">{T("Entrega *", "Delivery *")}</label><select id="checkout-delivery" name="delivery" required>{T("Envio para a morada", "Ship to my address", "option", attrs='value="shipping"')}{T("Levantamento no ateliê", "Studio collection", "option", attrs='value="pickup"')}</select></div>
    <div class="field" data-checkout-address><label for="checkout-address">{T("Morada completa (incluindo código postal e país) *", "Full address (including postal code and country) *")}</label><textarea id="checkout-address" name="address" autocomplete="street-address" rows="3" maxlength="500" required></textarea></div>
    <div class="field"><label for="checkout-notes">{T("Observações (opcional)", "Order notes (optional)")}</label><textarea id="checkout-notes" name="notes" rows="3" maxlength="1000"></textarea></div>
    <label class="check"><input type="checkbox" name="privacy" required><span>{T('Li como os meus dados são utilizados para responder a este pedido (<a class="link" href="privacidade.html">privacidade</a>).', 'I have read how my details are used to reply to this request (<a class="link" href="privacidade.html">privacy</a>).')}</span></label>
    <p class="form-note">{T("Os seus dados não são guardados no armazenamento do site. A disponibilidade, os portes e o pagamento serão confirmados pela Claudia. Este formulário não conclui uma compra.", "Your details are not saved in site storage. Claudia will confirm availability, shipping and payment. This form does not complete a purchase.")}</p>
    <button class="btn btn-solid" type="submit">{ICON["wa"]}{T("Continuar para o WhatsApp", "Continue to WhatsApp")}</button>
    <p class="form-note" data-checkout-status role="status" hidden>{T("Confirme o envio no WhatsApp. Se não abriu,", "Send your request in WhatsApp. If it did not open,")} <a class="link" data-checkout-link target="_blank" rel="noopener">{T("abra a mensagem aqui", "open the message here")}</a>.</p>
  </form>
</aside>
'''


ICON = {
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1-.3-.1-.5-.1-.7.1-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.1-1.3-.5-2.4-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5.7.3 1.3.5 1.7.6.7.2 1.4.2 1.9.1.6-.1 1.8-.7 2-1.4.2-.7.2-1.3.2-1.4-.1-.2-.3-.3-.6-.4M12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 0 1 12 2.2a9.8 9.8 0 0 1 0 19.6M12 0a12 12 0 0 0-10.3 18L0 24l6.2-1.6A12 12 0 1 0 12 0"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.6-1.6h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.4H7.3v3.2h2.8V22h3.4z"/></svg>',
    "tt": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 5.8A4.3 4.3 0 0 1 15.5 3h-3.1v12.4a2.6 2.6 0 1 1-2.6-2.6c.3 0 .5 0 .8.1V9.7a5.8 5.8 0 1 0 4.9 5.7V9.1a7.4 7.4 0 0 0 4.3 1.4V7.4a4.3 4.3 0 0 1-3.2-1.6z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "cart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 8h14l-1.2 11.1a2 2 0 0 1-2 1.9H8.2a2 2 0 0 1-2-1.9z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/></svg>',
    "hand": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 13V5.5a1.5 1.5 0 0 1 3 0V12m0-1V4.5a1.5 1.5 0 0 1 3 0V12m0-6.5a1.5 1.5 0 0 1 3 0V13m0-4.5a1.5 1.5 0 0 1 3 0V15a7 7 0 0 1-7 7h-1a7 7 0 0 1-5.6-2.8L3.2 15a1.6 1.6 0 0 1 2.5-2L8 15"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 20s-7.5-4.6-9.3-9.2C1.4 7.3 3.7 4 7 4c2 0 3.6 1.1 5 3 1.4-1.9 3-3 5-3 3.3 0 5.6 3.3 4.3 6.8C19.5 15.4 12 20 12 20z"/></svg>',
    "box": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m3 7 9-4 9 4v10l-9 4-9-4z"/><path d="m3 7 9 4 9-4M12 11v10"/></svg>',
    "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 2v6M12 16v6M2 12h6M16 12h6M5 5l4 4M15 15l4 4M19 5l-4 4M9 15l-4 4"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>',
}

NAV = [
    ("index.html", "Início", "Home"),
    ("sobre.html", "Sobre", "About"),
    ("servicos.html", "Serviços", "Services"),
    ("portfolio.html", "Portefólio", "Work"),
    ("loja.html", "Catálogo", "Catalogue"),
    ("contacto.html", "Contacto", "Contact"),
    ("faq.html", "Perguntas Frequentes", "FAQ"),
]

MSG_QUOTE = ("Olá Claudia! Vi o seu trabalho no site e gostava de pedir um orçamento para uma peça.",
             "Hi Claudia! I saw your work on the website and would like a quote for a piece.")
MSG_HELLO = ("Olá Claudia! Vim do site da Marclaro e tenho uma questão.",
             "Hi Claudia! I came from the Marclaro website and have a question.")


def head(file, title_pt, title_en, desc_pt, desc_en, img="hero.jpg"):
    def navlink(h, pt, en):
        cur = ' aria-current="page"' if h == file else ""
        return f'<a href="{h}"{cur}>{T(pt, en)}</a>'
    return f'''<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-en="{escape(title_en)}">{escape(title_pt)}</title>
<meta name="description" content="{escape(desc_pt)}" data-en="{escape(desc_en)}">
<link rel="canonical" href="{SITE}/{'' if file == 'index.html' else file}">
<link rel="alternate" hreflang="pt-PT" href="{SITE}/{'' if file == 'index.html' else file}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Claudia Sousa Art´s Marclaro">
<meta property="og:title" content="{escape(title_pt)}">
<meta property="og:description" content="{escape(desc_pt)}">
<meta property="og:image" content="{SITE}/img/{img}">
<meta property="og:locale" content="pt_PT"><meta property="og:locale:alternate" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFFFFF">
<link rel="icon" href="img/logo.png">
<link rel="stylesheet" href="css/style.css">
</head>
<body class="page-{file.removesuffix(".html")}">
<a class="skip" href="#main">Saltar para o conteúdo</a>
<header class="head">
  <div class="util"><div class="wrap">
    <p class="util-tag">{T("Feito à mão em Vila Nova de Gaia", "Handmade in Vila Nova de Gaia")}</p>
    <div class="util-r">
      <div class="lang" role="group" aria-label="Idioma / Language"><button data-lang="pt" aria-pressed="true">PT</button><button data-lang="en" aria-pressed="false">EN</button></div>
      {CART_BTN()}
      {WA("Pedir orçamento", "Request a quote", *MSG_QUOTE, cls="util-quote", icon=False)}
    </div>
  </div></div>
  <div class="wrap bar">
    <button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span></button>
    <a class="brand" href="index.html" aria-label="Marclaro — início"><img src="img/logo.png" alt="Claudia Sousa art´s marclaro — Handmade with love" width="120" height="54"></a>
    <nav class="nav" aria-label="Principal">
      <div class="nav-l">{"".join(navlink(h, pt, en) for h, pt, en in NAV[:3])}</div>
      <div class="nav-r">{"".join(navlink(h, pt, en) for h, pt, en in NAV[3:])}</div>
    </nav>
    {CART_BTN("cart-m")}
  </div>
</header>
<main id="main">
'''


def foot(on_shop=False):
    return f'''</main>
<footer class="foot">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img src="img/logo.png" alt="Marclaro" loading="lazy">
        <p>{T("Cerâmica e porcelana fria feitas à mão, aulas e experiências criativas em Vila Nova de Gaia.", "Handmade ceramics and cold porcelain, classes and creative experiences in Vila Nova de Gaia.")}</p>
        <div class="socials">
          <a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{ICON["ig"]}</a>
          <a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{ICON["fb"]}</a>
          <a href="{TT}" target="_blank" rel="noopener" aria-label="TikTok">{ICON["tt"]}</a>
        </div>
      </div>
      <div>
        <h4>{T("Explorar", "Explore")}</h4>
        <ul>{"".join(f'<li><a href="{h}">{T(pt, en)}</a></li>' for h, pt, en in NAV[1:])}</ul>
      </div>
      <div>
        <h4>{T("Contacto", "Contact")}</h4>
        <ul>
          <li><a href="https://wa.me/{WA_NUM}" data-wa="{escape(MSG_HELLO[0])}" data-wa-en="{escape(MSG_HELLO[1])}">WhatsApp</a></li>
          <li><a href="tel:+351919758281">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>São Félix da Marinha<br>Vila Nova de Gaia</li>
        </ul>
      </div>
      <div>
        <h4>{T("Informação legal", "Legal information")}</h4>
        <ul>
          <li><a href="privacidade.html">{T("Privacidade", "Privacy")}</a></li>
          <li><a href="cookies.html">{T("Cookies e armazenamento", "Cookies and storage")}</a></li>
          <li><a href="termos.html">{T("Termos e condições", "Terms and conditions")}</a></li>
          <li><a href="envios-devolucoes.html">{T("Envios e devoluções", "Shipping and returns")}</a></li>
          <li><a href="https://www.livroreclamacoes.pt/Inicio/" target="_blank" rel="noopener">{T("Livro de Reclamações", "Complaints Book")} ↗</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© <span class="year">2026</span> Claudia Sousa Art´s Marclaro. {T("Feito à mão, com carinho.", "Handmade, with love.")}</span>
      <span>{T("Um ateliê. Peças únicas. Feitas com tempo.", "One studio. Unique pieces. Made with time.")}</span>
    </div>
  </div>
</footer>

<a class="wa" href="https://wa.me/{WA_NUM}" data-wa="{escape(MSG_HELLO[0])}" data-wa-en="{escape(MSG_HELLO[1])}" aria-label="WhatsApp">{ICON["wa"]}<span data-en="Message me">Fale comigo</span></a>

{cart_drawer(on_shop)}
<script src="js/main.js" defer></script>
</body>
</html>
'''


def page_hero(eyebrow_pt, eyebrow_en, h_pt, h_en, lead_pt, lead_en, actions=""):
    return f'''<section class="page-hero"><div class="wrap">
  {T(eyebrow_pt, eyebrow_en, "p", "eyebrow eb-c")}
  {T(h_pt, h_en, "h1", "rv")}
  {T(lead_pt, lead_en, "p", "lead rv")}
{actions}
</div></section>'''


def band(h_pt, h_en, p_pt, p_en, second=None):
    sec = second or f'<a class="btn btn-line" href="servicos.html#reservar">{T("Reservar aula", "Book a class")}</a>'
    return f'''<section class="bg-dark band"><div class="wrap">
  {T("Vamos criar juntos", "Let’s make something", "p", "eyebrow eb-c")}
  {T(h_pt, h_en, "h2", "rv")}
  {T(p_pt, p_en, "p", "rv")}
  <div class="cta-row rv">{WA("Falar no WhatsApp", "Chat on WhatsApp", *MSG_QUOTE)}{sec}</div>
</div></section>'''


# ------------------------------------------------------------------ HOME
def home():
    works = [
        ("topo-casamento.jpg", "Topo de bolo de casamento em porcelana fria", "Cold porcelain wedding cake topper", "Porcelana fria", "Cold porcelain"),
        ("difusor.jpg", "Difusor de cerâmica perfurado à mão", "Hand-pierced ceramic diffuser", "Cerâmica", "Ceramics"),
        ("ursinho-baloao.jpg", "Ursinho em balão de ar quente, porcelana fria", "Teddy bear in a hot-air balloon, cold porcelain", "Peça personalizada", "Custom piece"),
        ("caneca-carolina.jpg", "Caneca personalizada com nome, pintada à mão", "Hand-painted personalised mug", "Personalizada", "Personalised"),
        ("presepio.jpg", "Presépio em porcelana fria", "Cold porcelain nativity scene", "Porcelana fria", "Cold porcelain"),
        ("figura-branca.jpg", "Figura esculpida em cerâmica", "Sculpted ceramic figure", "Cerâmica", "Ceramics"),
    ]
    rail = "".join(
        f'<a class="arch-card" href="portfolio.html"><div class="arch">{IMG(s, a, ae)}</div>'
        f'<div class="arch-meta"><span class="arch-idx">{i+1:02d}</span>{T(l, le, "span", "arch-cat")}</div>'
        f'{T(a, ae, "span", "arch-name")}</a>'
        for i, (s, a, ae, l, le) in enumerate(works))
    insta_imgs = ["figurinha-festa.jpg", "maos-tigela.jpg", "torno.jpg", "familias.jpg", "pintura-flor.jpg"]
    insta = "".join(f'<a href="{IG}" target="_blank" rel="noopener">{IMG(s, "Publicação do Instagram @marclaroarts", "Instagram post @marclaroarts")}</a>' for s in insta_imgs)
    svc = [
        ("pecas", "topo-casamento.jpg", "Peças personalizadas", "Custom pieces", "Topos de bolo, figuras, canecas e peças decorativas feitas à sua medida, a partir da sua ideia.", "Cake toppers, figurines, mugs and decorative pieces made to measure, from your idea."),
        ("aulas", "aula-grupo.jpg", "Aulas &amp; formação", "Classes &amp; training", "Cerâmica e porcelana fria, individual ou em grupo. Do primeiro contacto com a argila ao seu próprio projeto.", "Ceramics and cold porcelain, one-to-one or in groups. From first touching clay to your own project."),
        ("experiencias", "aula-pintura.jpg", "Experiências criativas", "Creative experiences", "Sessões curtas e descontraídas: aprende, experimenta e leva para casa a peça que fez.", "Short, relaxed sessions: learn, experiment and take home the piece you made."),
    ]
    more = T("Saber mais", "Learn more")
    orbit = "".join(
        f'<a class="orb rv" href="servicos.html#{i}"><span class="orb-n">0{k+1}</span><div class="orb-img">{IMG(s, pt, en)}</div>'
        f'{T(pt, en, "h3")}{T(dp, de, "p")}<span class="link">{more} &rarr;</span></a>'
        for k, (i, s, pt, en, dp, de) in enumerate(svc))
    return head("index.html",
                "Claudia Sousa Art´s Marclaro — Cerâmica e porcelana fria feitas à mão em Vila Nova de Gaia",
                "Claudia Sousa Art´s Marclaro — Handmade ceramics & cold porcelain in Vila Nova de Gaia",
                "Peças únicas em cerâmica e porcelana fria, feitas à mão em Vila Nova de Gaia. Encomendas personalizadas, aulas e experiências criativas.",
                "One-of-a-kind handmade ceramics and cold porcelain from Vila Nova de Gaia. Custom commissions, classes and creative experiences.") + f'''
<section class="hero-c"><div class="wrap">
  <div class="hero-text">
    {T("Ateliê em Vila Nova de Gaia · Porto", "Studio in Vila Nova de Gaia · Porto", "p", "eyebrow eb-c")}
    {T("Cerâmica e porcelana fria, <em>feitas à mão</em> em Vila Nova de Gaia.", "Handmade ceramics &amp; cold porcelain, <em>made in</em> Vila Nova de Gaia.", "h1")}
    {T("Peças únicas com alma, que contam histórias. Encomende a sua, ou venha aprender a fazê-la com as suas próprias mãos.", "One-of-a-kind pieces with soul, each telling a story. Commission yours, or come and learn to make it with your own hands.", "p", "lead")}
    <div class="cta-row cta-c">
      <a class="btn btn-solid" href="portfolio.html">{T("Ver o meu trabalho", "See my work")} &rarr;</a>
      {WA("Pedir orçamento", "Request a quote", *MSG_QUOTE, cls="btn btn-line")}
    </div>
  </div>
  <div class="trio">
    <div class="t-side t-l">{IMG("topo-casal.jpg", "Figura de casal em porcelana fria", "Cold porcelain couple figurine", lazy=False)}</div>
    <div class="t-main">

      <div class="t-circle">{IMG("torno.jpg", "Claudia Sousa a trabalhar uma peça na roda de oleiro", "Claudia Sousa shaping a piece on the banding wheel", lazy=False)}</div>

    </div>
    <div class="t-side t-r">{IMG("difusor.jpg", "Difusor de cerâmica perfurado", "Pierced ceramic diffuser", lazy=False)}</div>
  </div>
  <div class="facts-bar">
    <div><b>100%</b>{T("feito à mão", "handmade")}</div>
    <div><b>1/1</b>{T("não há duas iguais", "no two alike")}</div>
    <div><b>MB WAY</b>{T("pagamento simples", "easy payment")}</div>
  </div>
</div></section>



<section class="works-sec"><div class="wrap">
  <div class="split-head">
    <div>{T("Trabalhos selecionados", "Selected work", "p", "eyebrow")}{T("Peças que já <em>ganharam casa</em>", "Pieces that have <em>found a home</em>", "h2")}</div>
    <div>{T("Uma amostra de encomendas já entregues. Gosta de alguma? Peça-me uma semelhante, feita só para si.", "A sample of commissions already delivered. Like one? Ask me for something similar, made just for you.", "p")}
      <div class="rail-nav"><button class="rail-btn" data-dir="-1" aria-label="Anterior">&larr;</button><button class="rail-btn" data-dir="1" aria-label="Seguinte">&rarr;</button><a class="link" href="portfolio.html">{T("Ver portefólio completo", "View full portfolio")} &rarr;</a></div>
    </div>
  </div>
</div>
  <div class="rail" tabindex="0" aria-label="Trabalhos">{rail}</div>
  <div class="wrap"><div class="rail-line"><span></span></div></div>
</section>

<section class="ground"><div class="wrap about-c">
  <div class="portrait rv">

    <div class="p-circle">{IMG("atelier.jpg", "Claudia Sousa no seu ateliê", "Claudia Sousa in her studio")}</div>
  </div>
  <div class="about-txt rv">
    {T("Quem sou", "Who I am", "p", "eyebrow")}
    {T("Olá, sou a Claudia.", "Hi, I’m Claudia.", "h2")}
    <div class="about-p">
      {T("Trabalho a argila e a porcelana fria no meu ateliê em São Félix da Marinha, Vila Nova de Gaia. Cada peça nasce do gesto e do tempo: é moldada, seca, pintada e acabada à mão.", "I work with clay and cold porcelain in my studio in São Félix da Marinha, Vila Nova de Gaia. Every piece is born of gesture and time: shaped, dried, painted and finished by hand.", "p")}
      {T("As pequenas irregularidades não são defeitos. São a marca de que foi feita por alguém, para alguém.", "The small irregularities aren’t flaws. They are the mark that it was made by someone, for someone.", "p", "quote")}
    </div>
    <p class="sign">Claudia Sousa</p>
    <a class="btn btn-line" href="sobre.html">{T("Conhecer a minha história", "Read my story")} &rarr;</a>
  </div>
</div></section>

<section><div class="wrap">
  <div class="center-head">{T("O que faço", "What I do", "p", "eyebrow eb-c")}{T("Três formas de <em>trabalharmos juntos</em>", "Three ways to <em>work together</em>", "h2")}</div>
  <div class="orbits">{orbit}</div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="region">
    <div class="region-h">{T("A promessa Marclaro", "The Marclaro promise", "p", "eyebrow")}{T("Cuidado em <em>cada passo</em>", "Care at <em>every step</em>", "h2")}</div>
    <div class="quad">
      <div>{ICON["hand"]}<div>{T("Feito à mão", "Handmade", "h3")}{T("Todas as peças são 100% feitas à mão, por isso cada uma é única.", "Every piece is 100% handmade, so each one is unique.", "p")}</div></div>
      <div>{ICON["box"]}<div>{T("Embalagem cuidada", "Careful packaging", "h3")}{T("Embalagens personalizadas para que cada peça chegue intacta.", "Custom packaging so every piece arrives intact.", "p")}</div></div>
      <div>{ICON["star"]}<div>{T("Envio combinado", "Shipping, agreed with you", "h3")}{T("Peças prontas a enviar saem no dia que combinarmos, assim que o pagamento é confirmado.", "Ready-made pieces go out on the day we agree, once payment is confirmed.", "p")}</div></div>
      <div>{ICON["heart"]}<div>{T("Envio internacional", "International shipping", "h3")}{T("Enviamos para fora de Portugal, com portes sob orçamento.", "We ship outside Portugal, with shipping quoted on request.", "p")}</div></div>
    </div>
  </div>
</div></section>

<section><div class="wrap">
  <div class="center-head">{T("Siga o ateliê", "Follow the studio", "p", "eyebrow eb-c")}<h2>@marclaroarts</h2></div>
  <div class="insta-sym">{insta}</div>
  <div class="cta-row cta-c" style="margin-top:34px">
    <a class="btn btn-line btn-sm" href="{IG}" target="_blank" rel="noopener">{ICON["ig"]} Instagram</a>
    <a class="btn btn-line btn-sm" href="{FB}" target="_blank" rel="noopener">{ICON["fb"]} Facebook</a>
    <a class="btn btn-line btn-sm" href="{TT}" target="_blank" rel="noopener">{ICON["tt"]} TikTok</a>
  </div>
</div></section>
''' + band("Tem uma ideia? Vamos dar-lhe forma.", "Have an idea? Let’s give it shape.",
           "Envie-me uma mensagem com o que imagina, uma foto de referência ou a data do seu evento. Respondo pessoalmente.",
           "Send me a message with what you have in mind, a reference photo or your event date. I reply personally.") + foot()


# ------------------------------------------------------------------ ABOUT
def about():
    return head("sobre.html", "Sobre Claudia Sousa — Marclaro", "About Claudia Sousa — Marclaro",
                "Conheça Claudia Sousa, artesã de cerâmica e porcelana fria em Vila Nova de Gaia, e o ateliê Marclaro.",
                "Meet Claudia Sousa, ceramics and cold porcelain artisan in Vila Nova de Gaia, and the Marclaro studio.", "atelier.jpg") + \
        page_hero("Sobre", "About", "Peças com alma, <em>feitas por mãos</em> que gostam do que fazem.", "Pieces with soul, <em>made by hands</em> that love what they do.",
                  "A Marclaro é o ateliê de Claudia Sousa: um espaço calmo onde a argila e a porcelana fria se transformam em peças únicas, e onde quem chega aprende a fazer o mesmo.",
                  "Marclaro is Claudia Sousa’s studio: a calm space where clay and cold porcelain become unique pieces, and where visitors learn to do the same.") + f'''
<section class="ground"><div class="wrap about-c">
  <div class="portrait rv">

    <div class="p-circle">{IMG("torno.jpg", "Claudia Sousa a moldar uma taça", "Claudia Sousa shaping a bowl")}</div>
  </div>
  <div class="about-txt rv">
    {T("A minha história", "My story", "p", "eyebrow")}
    {T("Do gesto à peça", "From gesture to object", "h2")}
    <div class="about-p">
      {T("Comecei pela porcelana fria, a modelar pequenas figuras para as festas de amigos e família: topos de bolo, lembranças de batizado, presépios. Cada encomenda trazia uma história, e cada história pedia uma peça diferente.", "I started with cold porcelain, modelling small figures for friends’ and family celebrations: cake toppers, christening favours, nativity scenes. Every commission came with a story, and every story needed a different piece.", "p")}
      {T("Com o tempo chegou a cerâmica, com o forno, a roda e o barro. Hoje trabalho as duas técnicas lado a lado, no meu ateliê em São Félix da Marinha, Vila Nova de Gaia.", "In time ceramics followed, with the kiln, the wheel and the clay. Today I work both techniques side by side, in my studio in São Félix da Marinha, Vila Nova de Gaia.", "p")}
      {T("Num mundo cada vez mais feito em série, acredito em objetos que carregam o tempo e o cuidado de quem os fez, e que podem passar de geração em geração.", "In a world increasingly mass-produced, I believe in objects that carry the time and care of their maker, and can be passed down through generations.", "p")}
    </div>
    <p class="sign">Claudia</p>
  </div>
</div></section>

<section class="tight"><div class="wrap">
  <div class="region">
  <div class="region-h">{T("Valores", "Values", "p", "eyebrow")}{T("Aquilo em que acredito", "What I believe in", "h2")}</div>
  <div class="quad">
    <div>{ICON["hand"]}<div>{T("Feito à mão", "Handmade", "h3")}{T("Sem moldes industriais. Cada peça é trabalhada do início ao fim pelas minhas mãos.", "No industrial moulds. Every piece is worked from start to finish by my hands.", "p")}</div></div>
    <div>{ICON["heart"]}<div>{T("Dedicação", "Dedication", "h3")}{T("Tempo, paciência e técnica. Não apresso o barro, nem o processo.", "Time, patience and technique. I don’t rush the clay, or the process.", "p")}</div></div>
    <div>{ICON["star"]}<div>{T("Toque pessoal", "Personal touch", "h3")}{T("Ouço a sua história e transformo-a numa peça que é só sua.", "I listen to your story and turn it into a piece that is only yours.", "p")}</div></div>
    <div>{ICON["box"]}<div>{T("Proximidade", "Closeness", "h3")}{T("Um ateliê pequeno, sem pressas e sem pressão. Fala diretamente comigo.", "A small studio, unhurried and pressure-free. You talk directly to me.", "p")}</div></div>
  </div></div>
</div></section>

<section><div class="wrap">
  <div class="center-head">{T("O ateliê", "The studio", "p", "eyebrow eb-c")}{T("Onde tudo acontece", "Where it all happens", "h2")}
  {T("Mesas grandes, luz natural, prateleiras de peças a secar e um forno que trabalha a mais de 1000 °C.", "Big tables, natural light, shelves of drying pieces and a kiln that fires above 1000 °C.", "p")}</div>
  <div class="arch-grid">
    <figure class="arch rv">{IMG("atelier-sala.jpg", "Sala de trabalho do ateliê", "The studio workroom")}</figure>
    <figure class="arch rv">{IMG("maos-argila.jpg", "Mãos a trabalhar a argila", "Hands working clay")}</figure>
    <figure class="arch rv">{IMG("prateleira.jpg", "Peças a secar na prateleira", "Pieces drying on the shelf")}</figure>
    <figure class="arch rv">{IMG("forno.jpg", "Peças dentro do forno", "Pieces inside the kiln")}</figure>
    <figure class="arch rv">{IMG("escultura.jpg", "Pormenor de escultura em cerâmica", "Ceramic sculpture detail")}</figure>
  </div>
</div></section>
''' + band("Venha conhecer o ateliê.", "Come and visit the studio.",
           "Para uma encomenda, uma aula ou só para conversar sobre uma ideia: estou à distância de uma mensagem.",
           "For a commission, a class or just to talk through an idea: I’m one message away.") + foot()


# ------------------------------------------------------------------ SERVICES
def services():
    def svc(id_, tag_pt, tag_en, h_pt, h_en, p_pt, p_en, incl, imgs, cta, rev=False):
        li = "".join(T(a, b, "li") for a, b in incl)
        (m, ma, mb), *small = imgs
        sm = "".join(f'<div class="c-sm">{IMG(x, a, b)}</div>' for x, a, b in small)
        n = {"pecas": "01", "aulas": "02", "experiencias": "03"}[id_]
        return f'''<div class="svc2{' rev' if rev else ''}" id="{id_}">
  <div class="cluster rv">

    <div class="c-lg">{IMG(m, ma, mb)}</div>{sm}
    <span class="c-num">{n}</span>
  </div>
  <div class="svc-card rv">
    <div class="svc-top">{T(tag_pt, tag_en, "span", "tag")}{T(h_pt, h_en, "h2")}{T(p_pt, p_en, "p", "lead")}</div>
    <div class="svc-incl">{T("O que inclui", "What’s included", "p", "eyebrow")}<ul class="incl">{li}</ul></div>
    <div class="svc-cta">{cta}</div>
  </div>
</div>'''
    s1 = svc("pecas", "Sob orçamento", "Quoted on request", "Peças personalizadas", "Custom pieces",
             "Da ideia ao objeto: topos de bolo para casamentos e aniversários, lembranças de batizado e comunhão, figuras, canecas com nome e peças decorativas para a casa.",
             "From idea to object: cake toppers for weddings and birthdays, christening and communion favours, figurines, named mugs and decorative pieces for the home.",
             [("Conversa inicial para perceber a sua ideia (WhatsApp, email ou no ateliê)", "An initial chat to understand your idea (WhatsApp, email or at the studio)"),
              ("Orçamento claro e prazo definido antes de começar", "A clear quote and agreed timeline before I start"),
              ("Peça única em cerâmica ou porcelana fria, feita à mão", "A one-of-a-kind piece in ceramic or cold porcelain, handmade"),
              ("Fotos do processo, se quiser acompanhar", "Progress photos, if you’d like to follow along"),
              ("Embalagem protetora e envio ou levantamento no ateliê", "Protective packaging and shipping or studio pick-up")],
             [("topo-casamento.jpg", "Topo de bolo de noivos", "Bride and groom cake topper"), ("caneca-pers.jpg", "Caneca personalizada", "Personalised mug"), ("primeira-comunhao.jpg", "Lembrança de primeira comunhão", "First communion favour")],
             WA("Pedir orçamento", "Request a quote", "Olá Claudia! Gostava de pedir orçamento para uma peça personalizada. A minha ideia é:", "Hi Claudia! I’d like a quote for a custom piece. My idea is:"))
    s2 = svc("aulas", "Individual ou grupo", "One-to-one or group", "Aulas &amp; formação", "Classes &amp; training",
             "Aulas de cerâmica e de porcelana fria para quem quer começar do zero, aprofundar técnicas ou desenvolver o seu próprio projeto, com acompanhamento próximo.",
             "Ceramics and cold porcelain classes for complete beginners, those deepening their technique, or anyone developing their own project, with close guidance.",
             [("Técnicas de modelação manual, placas, rolos e escultura", "Hand-building techniques: slabs, coils and sculpture"),
              ("Decoração, pintura e vidragem das peças", "Decorating, painting and glazing your pieces"),
              ("Todos os materiais, ferramentas e cozeduras no forno", "All materials, tools and kiln firings"),
              ("Grupos pequenos para um acompanhamento verdadeiramente pessoal", "Small groups for truly personal guidance"),
              ("Formação à medida para quem quer aprofundar", "Tailored training for those who want to go further")],
             [("aula-grupo.jpg", "Aula de grupo no ateliê", "Group class at the studio"), ("aula-platos.jpg", "Aluna a trabalhar placas de argila", "Student working clay slabs"), ("aula-logotipo.jpg", "Pintura de caneca numa aula", "Painting a mug in class")],
             f'<a class="btn btn-solid" href="#reservar">{T("Pedir marcação", "Request a booking")} →</a>', rev=True)
    s3 = svc("experiencias", "Sessão única", "Single session", "Experiências criativas", "Creative experiences",
             "Duas ou três horas para desligar, sujar as mãos e criar. Ideal para amigos, famílias, aniversários, equipas ou turistas de passagem pelo Porto.",
             "Two or three hours to unplug, get your hands dirty and create. Perfect for friends, families, birthdays, teams or visitors passing through Porto.",
             [("Sem experiência necessária: eu guio cada passo", "No experience needed: I guide every step"),
              ("Uma peça criada por si (taça, prato, caneca ou figura)", "A piece made by you (bowl, plate, mug or figurine)"),
              ("Materiais, avental, cozedura e acabamento", "Materials, apron, firing and finishing"),
              ("Chá ou café e um ambiente calmo e acolhedor", "Tea or coffee in a calm, welcoming setting"),
              ("Sessões em português ou inglês", "Sessions in Portuguese or English")],
             [("pintura-flor.jpg", "Experiência de pintura em cerâmica", "Ceramic painting experience"), ("maos-tigela.jpg", "Mãos a moldar uma taça", "Hands shaping a bowl"), ("aula-pintura.jpg", "Participantes a pintar peças", "Participants painting pieces")],
             f'<a class="btn btn-solid" href="#reservar">{T("Reservar experiência", "Book an experience")} →</a>')
    return head("servicos.html", "Serviços — Peças personalizadas, aulas e experiências | Marclaro",
                "Services — Custom pieces, classes & experiences | Marclaro",
                "Peças personalizadas em cerâmica e porcelana fria, aulas individuais e de grupo e experiências criativas em Vila Nova de Gaia.",
                "Custom ceramic and cold porcelain pieces, private and group classes, and creative experiences in Vila Nova de Gaia.", "aula-grupo.jpg") + \
        page_hero("Serviços", "Services", "Encomende uma peça, <em>ou aprenda</em> a fazê-la.", "Commission a piece, <em>or learn</em> to make it.",
                  "Três formas de trazer o trabalho manual para a sua vida, sempre com calma, proximidade e atenção ao detalhe.",
                  "Three ways to bring handmade craft into your life, always calm, close and detail-minded.") + f'''
<nav class="pills" aria-label="Serviços"><a href="#pecas">{T("Peças personalizadas", "Custom pieces")}</a><a href="#aulas">{T("Aulas &amp; formação", "Classes &amp; training")}</a><a href="#experiencias">{T("Experiências criativas", "Creative experiences")}</a><a href="#reservar">{T("Reservar", "Book")}</a></nav>
<section style="padding-top:30px"><div class="wrap">{s1}{s2}{s3}</div></section>

<section class="bg-white"><div class="wrap">
  <div class="center-head">{T("Como funciona", "How it works", "p", "eyebrow eb-c")}{T("Simples, do início ao fim", "Simple, start to finish", "h2")}</div>
  <div class="steps">
    <div class="rv">{T("Fale comigo", "Get in touch", "h3")}{T("Envie uma mensagem pelo WhatsApp ou pelo formulário, com a sua ideia ou a data que prefere.", "Send a message on WhatsApp or via the form, with your idea or preferred date.", "p")}</div>
    <div class="rv">{T("Confirmamos juntos", "We confirm together", "h3")}{T("Respondo com orçamento, disponibilidade e todos os detalhes. Sem compromisso.", "I reply with a quote, availability and all the details. No obligation.", "p")}</div>
    <div class="rv">{T("Mãos à obra", "Hands on", "h3")}{T("Crio a sua peça, ou recebo-o no ateliê para criarmos juntos.", "I make your piece, or welcome you to the studio to make it together.", "p")}</div>
  </div>
</div></section>

<section id="reservar"><div class="wrap contact-grid">
  <div class="rv">
    {T("Marcações", "Bookings", "p", "eyebrow")}
    {T("Reserve a sua aula ou experiência", "Book your class or experience", "h2")}
    <div style="margin-top:22px">
      {T("Escolha o que procura e a data que prefere. Confirmo a disponibilidade pessoalmente por mensagem, normalmente no próprio dia.", "Choose what you’re after and your preferred date. I’ll personally confirm availability by message, usually the same day.", "p")}
      {T("Grupos, aniversários ou empresas? Indique o número de pessoas e preparo uma proposta.", "Groups, birthdays or companies? Tell me how many people and I’ll put together a proposal.", "p")}
    </div>
  </div>
  <form class="form rv" data-kind="booking" novalidate>
    <div class="two">
      <div class="field"><label for="b-nome">{T("Nome", "Name")} *</label><input id="b-nome" name="nome" required autocomplete="name"><span class="err">{T("Indique o seu nome.", "Please enter your name.")}</span></div>
      <div class="field"><label for="b-tel">{T("Telemóvel / WhatsApp", "Phone / WhatsApp")} *</label><input id="b-tel" name="telefone" type="tel" required autocomplete="tel" placeholder="+351 ..."><span class="err">{T("Indique um número válido.", "Please enter a valid number.")}</span></div>
    </div>
    <div class="two">
      <div class="field"><label for="b-srv">{T("O que procura", "What you’re after")} *</label>
        <select id="b-srv" name="servico" required>
          <option value="">—</option>
          <option value="aula-ceramica" data-en="Ceramics class">Aula de cerâmica</option>
          <option value="aula-porcelana" data-en="Cold porcelain class">Aula de porcelana fria</option>
          <option value="experiencia" data-en="Creative experience">Experiência criativa</option>
          <option value="grupo" data-en="Group / event / company">Grupo / evento / empresa</option>
          <option value="consulta" data-en="Consultation for a custom piece">Consulta para peça personalizada</option>
        </select><span class="err">{T("Escolha uma opção.", "Please choose an option.")}</span></div>
      <div class="field"><label for="b-fmt">{T("Formato", "Format")}</label>
        <select id="b-fmt" name="formato"><option value="individual" data-en="Individual">Individual</option><option value="grupo" data-en="Group">Grupo</option></select></div>
    </div>
    <div class="two">
      <div class="field"><label for="b-data">{T("Data preferida", "Preferred date")} *</label><input id="b-data" name="data" type="date" required><span class="err">{T("Escolha uma data.", "Please choose a date.")}</span></div>
      <div class="field"><label for="b-pax">{T("N.º de pessoas", "No. of people")}</label><input id="b-pax" name="pessoas" type="number" min="1" max="12" value="1"></div>
    </div>
    <div class="field"><label for="b-msg">{T("Notas", "Notes")}</label><textarea id="b-msg" name="notas" placeholder="Horário preferido, experiência anterior, ocasião…" data-en-ph="Preferred time, previous experience, occasion…"></textarea></div>
    <p class="form-note">{T("Este formulário abre o WhatsApp com os dados preenchidos. Só serão enviados quando confirmar a mensagem no WhatsApp. Se preferir, contacte-me por email.", "This form opens WhatsApp with your details filled in. They are only sent when you confirm the message in WhatsApp. You can also contact me by email.")}</p>
    <label class="check"><input type="checkbox" name="rgpd" required><span>{T('Li a informação sobre o tratamento dos meus dados para responder a este pedido (<a class="link" href="privacidade.html">privacidade</a>).', 'I have read how my details are used to reply to this request (<a class="link" href="privacidade.html">privacy</a>).')}</span></label>
    <button class="btn btn-solid" type="submit">{T("Enviar pedido de marcação", "Send booking request")}</button>
    <div class="ok" role="status">{T("O pedido está preparado. Confirme o envio no WhatsApp para que eu o possa receber.", "Your request is ready. Confirm sending it in WhatsApp so I can receive it.")}</div>
  </form>
</div></section>
''' + band("Ainda com dúvidas?", "Still have questions?",
           "Veja as perguntas frequentes ou envie-me uma mensagem. Respondo com todo o gosto.",
           "Check the FAQ or send me a message. I’m happy to help.",
           f'<a class="btn btn-line" href="faq.html">{T("Perguntas frequentes", "FAQ")}</a>') + foot()


# ------------------------------------------------------------------ PORTFOLIO
PORT = [
    ("topo-casamento.jpg", "porcelana personalizadas", "Topo de bolo de casamento", "Wedding cake topper"),
    ("difusor.jpg", "ceramica", "Difusor de cerâmica perfurado", "Pierced ceramic diffuser"),
    ("ursinho-baloao.jpg", "porcelana personalizadas", "Ursinho no balão de ar quente", "Teddy bear in a hot-air balloon"),
    ("aula-grupo.jpg", "aulas", "Aula de grupo no ateliê", "Group class at the studio"),
    ("figura-branca.jpg", "ceramica", "Figura esculpida em cerâmica", "Sculpted ceramic figure"),
    ("caneca-carolina.jpg", "ceramica personalizadas", "Caneca personalizada “Carolina”", "Personalised “Carolina” mug"),
    ("presepio.jpg", "porcelana", "Presépio em porcelana fria", "Cold porcelain nativity scene"),
    ("topo-casal.jpg", "porcelana personalizadas", "Casal de noivos em porcelana fria", "Cold porcelain bride and groom"),
    ("familias.jpg", "ceramica", "Família de figuras em cerâmica", "Family of ceramic figures"),
    ("pintura-flor.jpg", "aulas", "Pintura de peça numa experiência", "Painting a piece during an experience"),
    ("figurinha-festa.jpg", "porcelana personalizadas", "Topo de bolo de aniversário “Maria”", "“Maria” birthday cake topper"),
    ("bandeja.jpg", "ceramica", "Bandeja com motivo floral", "Tray with floral motif"),
    ("primeira-comunhao.jpg", "porcelana personalizadas", "Lembrança de primeira comunhão", "First communion keepsake"),
    ("maos-tigela.jpg", "aulas ceramica", "A moldar uma taça", "Shaping a bowl"),
    ("casamentos-bolos.jpg", "porcelana personalizadas", "Topos para bolo de casamento", "Wedding cake toppers"),
    ("presepio-argila.jpg", "ceramica", "Presépio em argila", "Clay nativity scene"),
    ("aula-platos.jpg", "aulas", "Trabalho com placas de argila", "Working with clay slabs"),
    ("caneca-pers.jpg", "ceramica personalizadas", "Caneca pintada à mão", "Hand-painted mug"),
    ("pintura-figura.jpg", "aulas porcelana", "Pintura de figura", "Painting a figurine"),
    ("escultura.jpg", "ceramica", "Escultura em cerâmica, pormenor", "Ceramic sculpture, detail"),
    ("aula-logotipo.jpg", "aulas personalizadas", "Personalizar uma caneca", "Personalising a mug"),
    ("forno.jpg", "ceramica", "Peças prontas para cozer", "Pieces ready for firing"),
]


def portfolio():
    items = "".join(f'<button class="item" data-cat="{c}">{IMG(s, pt, en)}{T(pt, en)}</button>' for s, c, pt, en in PORT)
    fl = [("all", "Tudo", "All"), ("ceramica", "Cerâmica", "Ceramics"), ("porcelana", "Porcelana fria", "Cold porcelain"),
          ("personalizadas", "Peças personalizadas", "Custom pieces"), ("aulas", "Aulas &amp; experiências", "Classes &amp; experiences")]
    fb = "".join(f'<button data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{T(a, b)}</button>' for k, a, b in fl)
    return head("portfolio.html", "Portefólio — Trabalhos em cerâmica e porcelana fria | Marclaro",
                "Portfolio — Ceramics & cold porcelain work | Marclaro",
                "Galeria de peças em cerâmica e porcelana fria feitas à mão: topos de bolo, figuras, canecas personalizadas, presépios e aulas.",
                "Gallery of handmade ceramic and cold porcelain pieces: cake toppers, figurines, personalised mugs, nativity scenes and classes.", "topo-casamento.jpg") + \
        page_hero("Portefólio · Claudia Sousa", "Portfolio · Claudia Sousa", "Um percurso feito <em>à mão.</em>", "A journey <em>made by hand.</em>",
                  "Da porcelana fria à cerâmica, das primeiras figuras à partilha no ateliê. O meu percurso, contado através das peças que crio.",
                  "From cold porcelain to ceramics, from the first figurines to sharing in the studio. My journey, told through the pieces I make.",
                  actions=f'<a class="link portfolio-jump" href="#trabalhos">{T("Explorar os trabalhos", "Explore the work")} ↓</a>') + f'''
<section class="journey" aria-labelledby="journey-title"><div class="wrap journey-grid">
  <figure>{IMG("torno.jpg", "Claudia Sousa a trabalhar a argila no ateliê", "Claudia Sousa working with clay in the studio", lazy=False)}<figcaption>{T("Claudia Sousa · Ateliê Marclaro, Vila Nova de Gaia", "Claudia Sousa · Marclaro studio, Vila Nova de Gaia")}</figcaption></figure>
  <div>
    {T("O meu percurso", "My journey", "p", "eyebrow")}
    {T("Dar forma. Criar memórias. Partilhar.", "Shaping. Making memories. Sharing.", "h2", attrs='id="journey-title"')}
    <ol class="journey-list">
      <li><span class="journey-number">01</span><div>{T("Os primeiros gestos", "The first gestures", "h3")}{T("Comecei pela porcelana fria, a modelar pequenas figuras para as festas de amigos e família. Topos de bolo, lembranças e presépios: cada peça nascia de uma história.", "I started with cold porcelain, modelling small figures for friends’ and family celebrations. Cake toppers, keepsakes and nativity scenes: each piece began with a story.", "p")}</div></li>
      <li><span class="journey-number">02</span><div>{T("O encontro com a cerâmica", "Discovering ceramics", "h3")}{T("Depois chegaram o barro, a roda e o forno. Hoje trabalho as duas técnicas lado a lado, explorando formas, texturas e acabamentos feitos à mão.", "Then came clay, the wheel and the kiln. Today I work with both techniques side by side, exploring handmade forms, textures and finishes.", "p")}</div></li>
      <li><span class="journey-number">03</span><div>{T("Um ateliê para partilhar", "A studio for sharing", "h3")}{T("Em São Félix da Marinha, o meu trabalho continua nas encomendas personalizadas e nas aulas e experiências de quem vem aprender comigo.", "In São Félix da Marinha, my work continues through custom commissions and classes and experiences for those who come to learn with me.", "p")}</div></li>
    </ol>
    <a class="link" href="sobre.html">{T("Conhecer melhor a minha história", "Read more of my story")} →</a>
  </div>
</div></section>
<section class="portfolio-work" id="trabalhos"><div class="wrap">
  <div class="split-head"><div>{T("Trabalhos selecionados", "Selected work", "p", "eyebrow")}{T("Peças, histórias e processos.", "Pieces, stories and processes.", "h2")}</div>{T("Encomendas realizadas e momentos de criação. Selecione uma categoria e abra cada fotografia para ver os detalhes.", "Completed commissions and moments of making. Choose a category and open a photograph to see the details.", "p")}</div>
  <div class="filters f-c" role="group" aria-label="Filtrar">{fb}</div>
  <div class="masonry grid-u">{items}</div>
  <div style="text-align:center;margin-top:50px">{WA("Quero uma peça assim", "I want a piece like this", "Olá Claudia! Vi o portefólio e gostava de uma peça semelhante a uma que vi no site.", "Hi Claudia! I saw your portfolio and would like a piece similar to one on the website.")}</div>
</div></section>
<div class="lb" role="dialog" aria-modal="true" aria-label="Imagem"><button class="x" aria-label="Fechar">×</button><button class="prev" aria-label="Anterior">‹</button><img alt=""><button class="next" aria-label="Seguinte">›</button><p></p></div>
''' + foot()


# ------------------------------------------------------------------ SHOP
# Edit products here: id, image, name PT, name EN, price (EUR), description PT, EN
PRODUCTS = [
    ("difusor", "difusor.jpg", "Difusor de aromas perfurado", "Pierced aroma diffuser", 38, "Cerâmica, feito à mão. Ø aprox. 14 cm.", "Handmade ceramic. Approx. Ø 14 cm."),
    ("bandeja", "bandeja.jpg", "Bandeja floral", "Floral tray", 32, "Cerâmica com relevo floral. Aprox. 25 × 15 cm.", "Ceramic with floral relief. Approx. 25 × 15 cm."),
    ("caneca", "caneca-pers.jpg", "Caneca pintada à mão", "Hand-painted mug", 24, "Pode ser personalizada com nome.", "Can be personalised with a name."),
    ("figura", "figura-branca.jpg", "Figura “Serenidade”", "“Serenity” figure", 45, "Escultura em cerâmica branca. Aprox. 22 cm.", "White ceramic sculpture. Approx. 22 cm."),
    ("familia", "familias.jpg", "Família em cerâmica", "Ceramic family", 55, "Conjunto de figuras sobre base de madeira.", "Set of figures on a wooden base."),
    ("presepio", "presepio-argila.jpg", "Presépio em argila", "Clay nativity", 60, "Peça única, pintada à mão.", "One-of-a-kind, hand-painted."),
]


def shop():
    cards = "".join(f'''<article class="prod rv" data-id="{i}" data-npt="{escape(pt)}" data-nen="{escape(en)}" data-price="{p}">
  <div class="img">{IMG(s, pt, en)}</div>
  <div class="body">{T(pt, en, "h3")}{T(dpt, den, "p", "muted")}<span class="price">{f"{p:.2f}".replace(".", ",")} €</span>
  <div class="row"><div class="qty"><button type="button" data-d="-1" aria-label="-">−</button><input type="number" value="1" min="1" max="20" aria-label="Quantidade"><button type="button" data-d="1" aria-label="+">+</button></div>
  <button class="btn btn-line add" type="button">{T("Adicionar", "Add to cart")}</button></div></div>
</article>''' for i, s, pt, en, p, dpt, den in PRODUCTS)
    return head("loja.html", "Catálogo — Peças de cerâmica feitas à mão | Marclaro", "Catalogue — Handmade ceramic pieces | Marclaro",
                "Descubra peças de cerâmica feitas à mão. Encomenda simples por WhatsApp e envio ou levantamento no ateliê.",
                "Discover handmade ceramic pieces. Simple ordering via WhatsApp, with delivery or studio pick-up.", "difusor.jpg") + \
        page_hero("Catálogo", "Catalogue", "Objetos feitos <em>com tempo.</em>", "Objects made <em>with time.</em>",
                  "Cerâmica feita à mão, peça a peça. Escolha as suas favoritas e confirme a disponibilidade comigo.",
                  "Handmade ceramics, piece by piece. Choose your favourites and check availability with me.") + f'''
<section style="padding-top:10px"><div class="wrap">
  <div class="catalogue-meta">{T("Peças em cerâmica", "Ceramic pieces", "p")}<span>{len(PRODUCTS)} {T("peças", "pieces")}</span></div>
  <div class="shop">{cards}</div>
  <details class="buying-info"><summary>{T("Como encomendar, pagamentos e entregas", "Ordering, payment and delivery")}</summary><div>{T('Adicione as peças ao carrinho e envie o pedido por WhatsApp. Antes de qualquer pagamento, confirmo a disponibilidade, o valor total com portes e o prazo. Pagamento por MB WAY ou transferência bancária. Pode combinar o levantamento no ateliê. Consulte os <a href="termos.html">termos e condições</a> e a política de <a href="envios-devolucoes.html">envios e devoluções</a>.', 'Add your pieces to the cart and send a request via WhatsApp. Before any payment, I confirm availability, the total including shipping and the timeline. Pay by MB WAY or bank transfer, or arrange studio collection. Read our <a href="termos.html">terms and conditions</a> and <a href="envios-devolucoes.html">shipping and returns policy</a>.', "p")}</div></details>
  <p class="muted" style="margin-top:36px;text-align:center">{T("Procura algo diferente?", "Looking for something different?")} <a class="link" href="servicos.html#pecas">{T("Peça uma peça personalizada", "Commission a custom piece")} →</a></p>
</div></section>
''' + foot(on_shop=True)


# ------------------------------------------------------------------ CONTACT
def contact():
    return head("contacto.html", "Contacto — Marclaro, Vila Nova de Gaia", "Contact — Marclaro, Vila Nova de Gaia",
                "Fale com Claudia Sousa: orçamentos, encomendas, aulas e experiências. WhatsApp +351 919 758 281. São Félix da Marinha, Vila Nova de Gaia.",
                "Get in touch with Claudia Sousa: quotes, orders, classes and experiences. WhatsApp +351 919 758 281. São Félix da Marinha, Vila Nova de Gaia.") + \
        page_hero("Contacto", "Contact", "Vamos <em>conversar.</em>", "Let’s <em>talk.</em>",
                  "O WhatsApp é a forma mais rápida. Se preferir, deixe-me uma mensagem aqui. Respondo sempre pessoalmente.",
                  "WhatsApp is the fastest way. If you prefer, leave me a message here. I always reply personally.") + f'''
<section style="padding-top:10px"><div class="wrap">
  <div class="contact-grid">
    <div class="cinfo panel-dark rv">{T("Fale comigo", "Talk to me", "p", "eyebrow")}
      <a href="https://wa.me/{WA_NUM}" data-wa="{escape(MSG_HELLO[0])}" data-wa-en="{escape(MSG_HELLO[1])}">{ICON["wa"]}<span><small>WhatsApp</small>{PHONE}</span></a>
      <a href="tel:+351919758281">{ICON["phone"]}<span><small>{T("Telefone", "Phone")}</small>{PHONE}</span></a>
      <a href="mailto:{EMAIL}">{ICON["mail"]}<span><small>Email</small>{EMAIL}</span></a>
      <div>{ICON["pin"]}<span><small>{T("Ateliê", "Studio")}</small>4410 São Félix da Marinha<br>Vila Nova de Gaia, Portugal</span></div>
      <p class="muted" style="font-size:.88rem;padding:6px 4px">{T("Visitas ao ateliê apenas por marcação.", "Studio visits by appointment only.")}</p>
      <div class="socials" style="margin:0">
        <a class="btn btn-line btn-sm" href="{IG}" target="_blank" rel="noopener">{ICON["ig"]}Instagram</a>
        <a class="btn btn-line btn-sm" href="{FB}" target="_blank" rel="noopener">{ICON["fb"]}Facebook</a>
        <a class="btn btn-line btn-sm" href="{TT}" target="_blank" rel="noopener">{ICON["tt"]}TikTok</a>
      </div>
    </div>
    <form class="form rv" data-kind="contact" novalidate>
      <div class="two">
        <div class="field"><label for="c-nome">{T("Nome", "Name")} *</label><input id="c-nome" name="nome" required autocomplete="name"><span class="err">{T("Indique o seu nome.", "Please enter your name.")}</span></div>
        <div class="field"><label for="c-email">Email *</label><input id="c-email" name="email" type="email" required autocomplete="email"><span class="err">{T("Indique um email válido.", "Please enter a valid email.")}</span></div>
      </div>
      <div class="field"><label for="c-ass">{T("Assunto", "Subject")} *</label>
        <select id="c-ass" name="assunto" required>
          <option value="">—</option>
          <option value="orcamento" data-en="Quote request">Pedido de orçamento</option>
          <option value="encomenda" data-en="Order">Encomenda</option>
          <option value="aulas" data-en="Classes &amp; experiences">Aulas &amp; experiências</option>
          <option value="outro" data-en="Other">Outro</option>
        </select><span class="err">{T("Escolha um assunto.", "Please choose a subject.")}</span></div>
      <div class="field"><label for="c-msg">{T("Mensagem", "Message")} *</label><textarea id="c-msg" name="mensagem" required placeholder="Conte-me a sua ideia, data ou dúvida…" data-en-ph="Tell me your idea, date or question…"></textarea><span class="err">{T("Escreva a sua mensagem.", "Please write your message.")}</span></div>
      <p class="form-note">{T("Este formulário abre o WhatsApp com os dados preenchidos. Só serão enviados quando confirmar a mensagem no WhatsApp. Se preferir, contacte-me por email.", "This form opens WhatsApp with your details filled in. They are only sent when you confirm the message in WhatsApp. You can also contact me by email.")}</p>
    <label class="check"><input type="checkbox" name="rgpd" required><span>{T('Li a informação sobre o tratamento dos meus dados para responder a esta mensagem (<a class="link" href="privacidade.html">privacidade</a>).', 'I have read how my details are used to reply to this message (<a class="link" href="privacidade.html">privacy</a>).')}</span></label>
      <button class="btn btn-solid" type="submit">{T("Enviar mensagem", "Send message")}</button>
      <div class="ok" role="status">{T("A mensagem está preparada. Confirme o envio no WhatsApp para que eu a possa receber.", "Your message is ready. Confirm sending it in WhatsApp so I can receive it.")}</div>
    </form>
  </div>
  <div class="map-link rv"><div>{T("Visite o ateliê", "Visit the studio", "h2")}{T("São Félix da Marinha, Vila Nova de Gaia. Visitas por marcação.", "São Félix da Marinha, Vila Nova de Gaia. Visits by appointment.", "p")}{T("O mapa abre num serviço externo, sujeito à política de privacidade da Google.", "The map opens on an external service, subject to Google's privacy policy.", "p", "muted")}</div><a class="btn btn-line" href="https://www.google.com/maps?q=São+Félix+da+Marinha,+Vila+Nova+de+Gaia,+Portugal" target="_blank" rel="noopener noreferrer">{T("Abrir mapa", "Open map")} ↗</a></div>
</div></section>
''' + foot()


# ------------------------------------------------------------------ FAQ
def faq():
    groups = [
        ("Peças &amp; encomendas", "Pieces &amp; orders", [
            ("É mesmo tudo feito à mão?", "Is everything really handmade?",
             "Sim, 100%. Cada peça é modelada, seca, pintada e acabada à mão no meu ateliê. Por isso tem pequenas irregularidades e nunca há duas iguais.",
             "Yes, 100%. Every piece is shaped, dried, painted and finished by hand in my studio. That’s why each has small irregularities and no two are alike."),
            ("Posso encomendar uma peça personalizada?", "Can I commission a custom piece?",
             "Claro. Envie-me a sua ideia pelo WhatsApp, de preferência com uma foto de referência, cores e a data de que precisa. Respondo com orçamento e prazo, sem compromisso.",
             "Of course. Send me your idea on WhatsApp, ideally with a reference photo, colours and the date you need it. I’ll reply with a quote and timeline, no obligation."),
            ("Quais são os prazos de produção?", "What are the lead times?",
             "Depende da peça. Peças em porcelana fria demoram normalmente 2 a 3 semanas. Cerâmica, que precisa de secar e ir ao forno, 3 a 5 semanas. Para eventos, fale comigo com a maior antecedência possível.",
             "It depends on the piece. Cold porcelain usually takes 2–3 weeks. Ceramics, which need to dry and be kiln-fired, take 3–5 weeks. For events, get in touch as early as you can."),
            ("Fazem entregas?", "Do you deliver?",
             "Sim. Assim que o pagamento é confirmado, envio a peça em embalagem protetora personalizada, na data que combinarmos. Também pode levantar no ateliê em São Félix da Marinha. Envio internacional com portes sob orçamento por email.",
             "Yes. Once payment is confirmed I send the piece in custom protective packaging, agreeing the day with you. You can also collect from the studio in São Félix da Marinha. International shipping is quoted by email."),
            ("Como posso pagar?", "How can I pay?",
             "MB WAY ou transferência bancária. Nas encomendas personalizadas é pedido um sinal para iniciar o trabalho.",
             "MB WAY or bank transfer. Custom commissions require a deposit to begin."),
        ]),
        ("Aulas &amp; experiências", "Classes &amp; experiences", [
            ("O que está incluído numa aula?", "What’s included in a class?",
             "Todos os materiais (argila ou porcelana fria, tintas, vidrados), ferramentas, avental, cozedura no forno e acompanhamento. Só precisa de trazer vontade e roupa que possa sujar.",
             "All materials (clay or cold porcelain, paints, glazes), tools, apron, kiln firing and guidance. Just bring curiosity and clothes you don’t mind getting dirty."),
            ("Preciso de ter experiência?", "Do I need experience?",
             "Não. As aulas e experiências são pensadas para quem nunca tocou em argila. Quem já tem prática pode aprofundar técnicas ou desenvolver o seu projeto.",
             "No. Classes and experiences are designed for people who have never touched clay. Those with experience can deepen their technique or develop their own project."),
            ("Qual o tamanho mínimo e máximo dos grupos?", "What’s the minimum and maximum group size?",
             "As aulas podem ser individuais (1 pessoa). Os grupos têm até 8 pessoas, para que todos tenham acompanhamento. Para grupos maiores, eventos ou empresas, preparo uma proposta à medida.",
             "Classes can be one-to-one. Groups have up to 8 people so everyone gets attention. For larger groups, events or companies, I’ll prepare a tailored proposal."),
            ("Quando levo a minha peça para casa?", "When do I take my piece home?",
             "As peças de porcelana fria podem ir consigo no próprio dia. As de cerâmica precisam de secar e ir ao forno, e ficam prontas para levantar (ou enviar) em cerca de 2 a 3 semanas.",
             "Cold porcelain pieces can go home with you the same day. Ceramic pieces need to dry and be fired, and are ready to collect (or ship) in about 2–3 weeks."),
            ("As aulas são em inglês?", "Are classes in English?",
             "Sim, as sessões podem ser em português ou em inglês. Ideal para quem está de visita ao Porto.",
             "Yes, sessions can be in Portuguese or English. Perfect for visitors to Porto."),
            ("Como reservo e qual a política de cancelamento?", "How do I book, and what’s the cancellation policy?",
             "Reserve pelo formulário na página Serviços ou pelo WhatsApp. Confirmo a data por mensagem. Pode cancelar ou reagendar sem custos até 48 horas antes. Com menos antecedência, tentamos encontrar outra data; as condições do sinal são comunicadas antes da reserva, sem prejuízo dos seus direitos legais. Consulte os <a href='termos.html'>termos e condições</a>.",
             "Book via the form on the Services page or on WhatsApp. I’ll confirm the date by message. You can cancel or reschedule free of charge up to 48 hours before. With less notice, we try to find another date; deposit conditions are explained before booking, without affecting your legal rights. Read the <a href='termos.html'>terms and conditions</a>."),
        ]),
    ]
    body = ""
    for k, (gpt, gen, qs) in enumerate(groups):
        items = "".join(f'<details class="rv"><summary>{T(q, qe)}</summary><div>{T(a, ae, "p")}</div></details>' for q, qe, a, ae in qs)
        body += f'<div class="faq-sec"><div class="faq-side"><span class="faq-n">0{k+1}</span>{T(gpt, gen, "h2")}<p class="muted">{len(qs)} {T("perguntas", "questions")}</p></div><div class="faq-list">{items}</div></div>'
    return head("faq.html", "Perguntas Frequentes | Marclaro", "FAQ | Marclaro",
                "Respostas sobre peças feitas à mão, encomendas personalizadas, prazos, envios, aulas e experiências de cerâmica em Vila Nova de Gaia.",
                "Answers about handmade pieces, custom commissions, lead times, shipping, ceramics classes and experiences in Vila Nova de Gaia.") + \
        page_hero("Perguntas frequentes", "FAQ", "Tudo o que <em>precisa de saber.</em>", "Everything <em>you need to know.</em>",
                  "Não encontra a sua resposta? Envie-me uma mensagem, que respondo com gosto.",
                  "Can’t find your answer? Send me a message, I’m happy to help.") + f'''
<section style="padding-top:10px"><div class="wrap"><div class="faq2">{body}</div></div></section>
''' + band("Ainda tem dúvidas?", "Still wondering?", "Fale diretamente comigo, sem compromisso.", "Talk to me directly, no obligation.",
           f'<a class="btn btn-line" href="contacto.html">{T("Página de contacto", "Contact page")}</a>') + foot()


# ------------------------------------------------------------------ LEGAL
# Shared legal layout; bilingual copy and publication flags live in legal_content.py.
def legal_page(file):
    content = LEGAL_PAGES[file]
    pt, en = content["title"]
    intro_pt, intro_en = content["intro"]
    nav = '<nav class="legal-nav" aria-label="Informação legal / Legal information">' + "".join(
        f'<a href="{url}"' + (' aria-current="page"' if url == file else '') + f'>{T(*data["title"])}</a>'
        for url, data in LEGAL_PAGES.items()) + '</nav>'
    note = T("Versão de preparação: antes da publicação comercial, é necessário confirmar a identificação fiscal, a morada profissional e de devolução, os preços e a informação de reclamações e resolução de litígios. Estas condições devem ser revistas pelo responsável do ateliê.",
             "Pre-launch version: before commercial publication, tax identification, professional and return addresses, prices, and complaints and dispute resolution information must be confirmed. These terms should be reviewed by the studio owner.", "p", "legal-note") if content.get("draft") else ""
    sections = "".join(T(hpt, hen, "h2") + T(bpt, ben, "p") for hpt, hen, bpt, ben in content["sections"])
    extra = ""
    if file == "cookies.html":
        extra = f'''<h2>{T("Dados guardados neste navegador", "Data saved in this browser")}</h2>
<dl class="storage-list">
  <div><dt>mc-lang</dt><dd>{T("Preferência de idioma (PT ou EN), guardada quando escolhe o idioma. Funcional; permanece até ser apagada.", "Language preference (PT or EN), saved when you choose a language. Functional; kept until cleared.")}</dd></div>
  <div><dt>mc-cart</dt><dd>{T("Peças e quantidades do carrinho, guardadas quando adiciona ou remove uma peça. Necessário ao carrinho solicitado; permanece até ser apagado. Não inclui nome, email, morada ou dados de pagamento.", "Cart pieces and quantities, saved when you add or remove an item. Necessary for the requested cart; kept until cleared. Does not include your name, email, address or payment details.")}</dd></div>
</dl>
<p>{T("Pode apagar o idioma e esvaziar o carrinho neste navegador com o botão abaixo. Também pode bloquear o armazenamento nas definições do navegador; nesse caso, as escolhas podem perder-se ao mudar de página.", "Use the button below to clear your saved language and empty the cart in this browser. You can also block storage in browser settings; choices may then be lost between pages.")}</p>
<button class="btn btn-line" type="button" data-clear-storage style="margin-top:24px">{T("Apagar idioma e esvaziar carrinho", "Clear language and empty cart")}</button>
<p data-storage-status role="status" aria-live="polite"></p>'''
    elif file == "envios-devolucoes.html":
        extra = f'''<div class="withdrawal">
{T("Modelo de comunicação de livre resolução", "Withdrawal notification template", "h2")}
{T('Para: Claudia Sousa Art´s Marclaro — <a href="mailto:claudimar60@gmail.com">claudimar60@gmail.com</a>.', 'To: Claudia Sousa Art´s Marclaro — <a href="mailto:claudimar60@gmail.com">claudimar60@gmail.com</a>.', "p")}
{T("Comunico que resolvo o contrato de compra relativo à seguinte peça: [identificação]. Encomendada em: [data]. Recebida em: [data]. Nome do consumidor: [nome]. Endereço do consumidor: [endereço]. Data: [data]. Assinatura: [apenas se enviada em papel].", "I hereby withdraw from the purchase contract for the following item: [identification]. Ordered on: [date]. Received on: [date]. Consumer name: [name]. Consumer address: [address]. Date: [date]. Signature: [only for paper submissions].", "p")}
</div>'''
    return head(file, pt + " | Marclaro", en + " | Marclaro", intro_pt, intro_en) + \
        page_hero("Informação legal", "Legal information", pt, en, intro_pt, intro_en) + f'''
<section style="padding-top:10px"><div class="wrap prose">
{nav}{note}
{T("Última atualização: 26 de setembro de 2026.", "Last updated: 26 September 2026.", "p", "muted")}
{sections}{extra}
</div></section>
''' + foot()


PAGES = {"index.html": home, "sobre.html": about, "servicos.html": services, "portfolio.html": portfolio,
         "loja.html": shop, "contacto.html": contact, "faq.html": faq}
PAGES.update({file: (lambda file=file: legal_page(file)) for file in LEGAL_PAGES})

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for f, fn in PAGES.items():
        open(f, "w", encoding="utf-8").write(fn())
    urls = "".join(f"<url><loc>{SITE}/{'' if f == 'index.html' else f}</loc></url>" for f in PAGES)
    open("sitemap.xml", "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open("robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
    print("Built", len(PAGES), "pages")
