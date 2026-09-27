# Guide: Marclaro website

## Structure
- `build.py` holds all the text (PT and EN) and generates the 8 HTML pages. After editing it, run `python3 build.py`.
- `css/style.css` is the design (colour palette at the top). `js/main.js` handles language, cart, forms, lightbox and cookies.
- `img/` holds the photos, already compressed.

## Swapping photos (after the photo shoot)
Save the new photo in `img/` **with the same name** as the old one (e.g. `torno.jpg`) and it updates across the whole site. Recommended: JPG, max. 1600 px, under 400 KB.

## Shop
The shop mirrors the **WhatsApp Business catalog** (https://wa.me/c/149207197470727): in `build.py`, edit the `SHOP` list — categories, each with items `(id, image, PT name, EN name, price, PT desc, EN desc)`.
- Use `None` as the price to show “Sob consulta / Price on request” (the cart total then shows “A combinar / To be agreed”). **Set your real prices when you have them.**
- `img/brinco-1…5.jpg` and `img/presepio-3.jpg` are generated placeholders (see `img/_make_placeholders.py`) — replace them with the real photos, same names, when you have them.
- After editing, run `python3 build.py`. The cart sends the order through WhatsApp; you confirm payment by MB WAY or bank transfer.
The cart panel (the `cart_drawer()` helper in `build.py`) is part of the shared footer, so it exists on **every**
page and the basket icon in the header just opens it wherever the visitor is — only the product grid lives on
`loja.html`. The basket itself is kept in the visitor's browser (localStorage), so the items are still there when
they move between pages.

## Portfolio
In `build.py`, the `PORT` list: image, categories (`ceramica`, `porcelana`, `personalizadas`, `aulas`), PT caption, EN caption.

## Messages and bookings
Without a server, the contact and booking forms open WhatsApp with the request already filled in.
To receive them by email instead: create a free form on https://formspree.io, copy the URL and add
`data-endpoint="https://formspree.io/f/XXXX"` to the `<form ...>` tags in `build.py`.

## Domain, hosting and email
1. **Domain:** register `marclaroarts.pt` (e.g. at PTisp, Amen.pt or Dominios.pt, about €15 per year).
2. **Hosting (free):** Netlify or Cloudflare Pages. Drag the `marclaro` folder into Netlify (app.netlify.com/drop), or connect your GitHub repository so every change goes live automatically. Point the domain to it in the DNS settings.
3. **Email ola@marclaroarts.pt:** Zoho Mail (free plan) or the domain registrar's email service.
4. **Statistics:** create an account at plausible.io with the domain marclaroarts.pt. It only loads after the visitor accepts cookies.
