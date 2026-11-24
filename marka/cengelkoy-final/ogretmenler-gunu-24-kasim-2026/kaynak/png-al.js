// Kullanim: node kaynak/png-al.js <cikti-klasoru>   (hikaye-1..4.html -> 1080x1920 PNG)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const out = process.argv[2] || '.';
  const root = path.resolve(__dirname, '..');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  for (let i = 1; i <= 4; i++) {
    await p.goto('file://' + path.join(root, `hikaye-${i}.html`));
    await p.waitForLoadState('load');
    await p.screenshot({ path: path.join(out, `hikaye-${i}.png`) });
  }
  await b.close();
})();
