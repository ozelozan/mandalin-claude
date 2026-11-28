// Kullanim: node kaynak/png-al.js [cikti-klasoru]   (hikaye-*.html -> 1080x1920 PNG, Playwright)
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const kok = path.resolve(__dirname, '..'); const out = path.resolve(process.argv[2] || path.join(kok, 'png'));
fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (const f of fs.readdirSync(kok).filter(n => /^hikaye-\d+\.html$/.test(n)).sort()) {
    await pg.goto('file://' + path.join(kok, f) + '#png', { waitUntil: 'networkidle' });
    await pg.evaluate(() => document.fonts.ready); await pg.waitForTimeout(300);
    const o = path.join(out, f.replace('.html', '.png')); await pg.screenshot({ path: o }); console.log(o);
  }
  await b.close();
})();
