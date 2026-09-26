const { test, expect } = require('@playwright/test');
const fs = require('node:fs');
const pages = fs.readdirSync('.').filter(file => file.endsWith('.html'));

for (const file of pages) {
  test(`${file}: loads locally, accessible headings, no overflow or external requests`, async ({ page }) => {
    const errors = [], remote = [], failures = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('request', req => { if (!new URL(req.url()).hostname.match(/^(127\.0\.0\.1|localhost)$/)) remote.push(req.url()); });
    page.on('response', res => { if (res.status() >= 400) failures.push(res.url()); });
    await page.goto('/' + file);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(255, 255, 255)');
    // Load every lazy image and verify the actual asset, not just the placeholder.
    await page.locator('img[loading="lazy"]').evaluateAll(images => images.forEach(img => img.loading = 'eager'));
    await expect.poll(() => page.locator('img[src]').evaluateAll(images => images.every(img => img.complete && img.naturalWidth > 0))).toBe(true);
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
    expect(await page.locator('.ring, .stamp, .ph-ring, iframe, .cookie, .news').count()).toBe(0);
    for (const policy of ['privacidade.html', 'cookies.html', 'termos.html', 'envios-devolucoes.html']) {
      await expect(page.locator(`.foot a[href="${policy}"]`)).toBeVisible();
    }
    await page.locator('[data-lang="en"]').click();
    await expect(page.locator('html')).toHaveAttribute('lang', 'en');
    await page.locator('[data-lang="pt"]').click();
    await expect(page.locator('html')).toHaveAttribute('lang', 'pt-PT');
    expect(errors).toEqual([]);
    expect(remote).toEqual([]);
    expect(failures).toEqual([]);
  });
}

test('portfolio journey, filters and keyboard lightbox', async ({ page }) => {
  await page.goto('/portfolio.html');
  await expect(page.locator('.journey-list li')).toHaveCount(3);
  await page.locator('[data-filter="porcelana"]').click();
  await expect(page.locator('[data-filter="porcelana"]')).toHaveAttribute('aria-pressed', 'true');
  expect(await page.locator('.masonry .item:not(.hide)').evaluateAll(items => items.every(item => item.dataset.cat.includes('porcelana')))).toBe(true);
  const first = page.locator('.masonry .item:not(.hide)').first();
  await first.click();
  await expect(page.locator('.lb')).toBeVisible();
  await expect(page.locator('.lb img')).toHaveAttribute('src', /topo-casamento/);
  await page.keyboard.press('ArrowRight');
  await expect(page.locator('.lb img')).toHaveAttribute('src', /ursinho/);
  await page.keyboard.press('Shift+Tab');
  await expect(page.locator('.lb .next')).toBeFocused();
  await page.keyboard.press('Escape');
  await expect(page.locator('.lb')).not.toBeVisible();
  await expect(first).toBeFocused();
  await page.locator('[data-filter="all"]').click();
  await expect(page.locator('.masonry .item:not(.hide)')).toHaveCount(22);
});

test('catalogue, cart persistence, quote hand-off and storage deletion', async ({ page }) => {
  await page.goto('/loja.html');
  await expect(page.locator('.prod')).toHaveCount(6);
  await page.locator('.prod').first().locator('.qty input').fill('2');
  await page.locator('.prod').first().locator('.add').click();
  await expect(page.locator('#cart')).toHaveAttribute('aria-hidden', 'false');
  await expect(page.locator('#cart .total b')).toHaveText(/76,00/);
  await expect(page.locator('#cart a[href="termos.html"]')).toBeVisible();
  await page.evaluate(() => { window.open = url => { window.testOutgoing = url; }; });
  await page.locator('.checkout').click();
  const checkout = page.locator('#checkout-form');
  await expect(checkout).toBeVisible();
  await expect(checkout.locator('[name="name"]')).toBeFocused();
  expect(await page.evaluate(() => window.testOutgoing)).toBeUndefined();
  await checkout.locator('[type="submit"]').click();
  expect(await page.evaluate(() => window.testOutgoing)).toBeUndefined();
  await checkout.locator('[name="name"]').fill('Ana Sousa');
  await checkout.locator('[name="email"]').fill('ana@example.com');
  await checkout.locator('[name="phone"]').fill('+351 919 123 456');
  await checkout.locator('[name="privacy"]').check();
  await checkout.locator('[type="submit"]').click();
  expect(await page.evaluate(() => window.testOutgoing)).toBeUndefined();
  await expect(checkout.locator('[name="address"]')).toBeFocused();
  await checkout.locator('[name="address"]').fill('Rua das Flores 12, 4400-001 Gaia, Portugal');
  await checkout.locator('[name="notes"]').fill('Embrulho para presente & cartão');
  await checkout.locator('[type="submit"]').click();
  const outgoing = await page.evaluate(() => new URL(window.testOutgoing).searchParams.get('text'));
  for (const detail of ['2 × Difusor', '76,00', 'Ana Sousa', 'ana@example.com', '+351 919 123 456', 'Rua das Flores 12', 'Embrulho para presente & cartão']) {
    expect(outgoing).toContain(detail);
  }
  await expect(checkout.locator('[data-checkout-status]')).toBeVisible();
  await expect(checkout.locator('[data-checkout-link]')).toHaveAttribute('href', await page.evaluate(() => window.testOutgoing));
  expect(await page.evaluate(() => JSON.stringify(localStorage))).not.toContain('ana@example.com');
  await page.keyboard.press('Escape');
  await page.goto('/sobre.html');
  await page.locator('.cart-btn:visible').click();
  await expect(page.locator('.ci')).toHaveCount(1);
  await page.keyboard.press('Escape');
  await page.goto('/cookies.html');
  await page.locator('[data-lang="en"]').click();
  await page.locator('[data-clear-storage]').click();
  await expect(page.locator('[data-storage-status]')).toContainText('cart is empty');
  expect(await page.evaluate(() => ['mc-cart', 'mc-lang', 'mc-consent'].map(key => localStorage.getItem(key)))).toEqual([null, null, null]);
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('lang', 'pt-PT');
  await page.locator('.cart-btn:visible').click();
  await expect(page.locator('.checkout')).toBeDisabled();
});

test('no tracking for legacy consent and usable when storage is blocked', async ({ page }) => {
  const scripts = [];
  page.on('request', req => { if (req.resourceType() === 'script') scripts.push(req.url()); });
  await page.addInitScript(() => localStorage.setItem('mc-consent', 'yes'));
  await page.goto('/privacidade.html');
  expect(await page.evaluate(() => localStorage.getItem('mc-consent'))).toBeNull();
  expect(scripts.every(url => url.endsWith('/js/main.js'))).toBe(true);
  await page.addInitScript(() => {
    Object.defineProperty(window, 'localStorage', { get() { throw new Error('Storage blocked'); } });
  });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto('/loja.html');
  await page.locator('[data-lang="en"]').click();
  await expect(page.locator('html')).toHaveAttribute('lang', 'en');
  await page.locator('.add').first().click();
  await expect(page.locator('.ci')).toHaveCount(1);
  expect(errors).toEqual([]);
});

test('contact form validates and opens a request, not a silent submission', async ({ page }) => {
  await page.goto('/contacto.html');
  await page.evaluate(() => { window.open = url => { window.testOutgoing = url; }; });
  const form = page.locator('form[data-kind="contact"]');
  await form.locator('[type="submit"]').click();
  expect(await page.evaluate(() => window.testOutgoing)).toBeUndefined();
  await form.locator('input[name="nome"]').fill('Teste Marclaro');
  await form.locator('input[type="email"]').fill('teste@example.com');
  const phone = form.locator('input[type="tel"]');
  if (await phone.count()) await phone.fill('919123456');
  await form.locator('select').selectOption({ index: 1 });
  await form.locator('textarea').fill('Gostava de saber mais sobre uma peça.');
  await form.locator('[name="rgpd"]').check();
  await form.locator('[type="submit"]').click();
  expect(await page.evaluate(() => window.testOutgoing)).toMatch(/^https:\/\/wa.me\/351919758281\?text=/);
  await expect(form.locator('.ok')).toContainText('Confirme o envio no WhatsApp');
});

test('mobile menu exposes the catalogue link', async ({ page, isMobile }) => {
  test.skip(!isMobile);
  await page.goto('/index.html');
  await page.locator('.burger').click();
  await expect(page.locator('.nav')).toHaveClass(/open/);
  await page.locator('.nav a[href="loja.html"]').click();
  await expect(page).toHaveURL(/loja.html$/);
});

test('internal links and fragment targets exist', async ({ page }) => {
  const html = Object.fromEntries(pages.map(file => [file, fs.readFileSync(file, 'utf8')]));
  for (const file of pages) {
    await page.goto('/' + file);
    const links = await page.locator('a[href]').evaluateAll(anchors => anchors.map(anchor => anchor.getAttribute('href')));
    for (const href of links) {
      if (/^(https?:|mailto:|tel:)/.test(href)) continue;
      const [path, hash] = href.split('#');
      const target = path.split('?')[0] || file;
      expect(html[target], `${file}: broken link ${href}`).toBeDefined();
      if (hash) expect(html[target], `${file}: missing fragment ${href}`).toContain(`id="${hash}"`);
    }
  }
});


test('checkout supports collection, back navigation and keyboard focus on other pages', async ({ page }) => {
  await page.goto('/loja.html');
  await page.locator('.add').first().click();
  await page.keyboard.press('Escape');
  await page.goto('/sobre.html');
  await page.locator('[data-lang="en"]').click();
  await page.locator('.cart-btn:visible').click();
  await page.locator('.checkout').click();
  const form = page.locator('#checkout-form');
  await expect(form.locator('h3')).toHaveText('Order details');
  await form.locator('[name="name"]').fill('Jane Smith');
  await form.locator('[data-checkout-back]').click();
  await expect(form).toBeHidden();
  await expect(page.locator('.checkout')).toBeFocused();
  await page.locator('.checkout').click();
  await expect(form.locator('[name="name"]')).toHaveValue('Jane Smith');
  await form.locator('[name="delivery"]').selectOption('pickup');
  await expect(form.locator('[name="address"]')).toBeHidden();
  await form.locator('[name="email"]').fill('invalid');
  await form.locator('[name="phone"]').fill('020 1234 5678');
  await form.locator('[name="privacy"]').check();
  await page.evaluate(() => { window.open = url => { window.testOutgoing = url; }; });
  await form.locator('[type="submit"]').click();
  expect(await page.evaluate(() => window.testOutgoing)).toBeUndefined();
  await form.locator('[name="email"]').fill('jane@example.com');
  await form.locator('[name="privacy"]').uncheck();
  await form.locator('[type="submit"]').click();
  expect(await page.evaluate(() => window.testOutgoing)).toBeUndefined();
  await form.locator('[name="privacy"]').check();
  await form.locator('[type="submit"]').click();
  const message = await page.evaluate(() => new URL(window.testOutgoing).searchParams.get('text'));
  expect(message).toContain('Delivery: Studio collection');
  expect(message).toContain('Jane Smith');
  expect(message).not.toContain('Address:');
  await form.locator('[data-checkout-link]').focus();
  await page.keyboard.press('Tab');
  await expect(page.locator('#cart header button')).toBeFocused();
  await page.keyboard.press('Shift+Tab');
  await expect(form.locator('[data-checkout-link]')).toBeFocused();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
  await page.keyboard.press('Escape');
  await expect(page.locator('.cart-btn:visible')).toBeFocused();
  await page.locator('.cart-btn:visible').click();
  await page.locator('[data-rm]').click();
  await expect(page.locator('.checkout')).toBeDisabled();
  await expect(form).toBeHidden();
  await expect(form.locator('[name="name"]')).toHaveValue('');
});
