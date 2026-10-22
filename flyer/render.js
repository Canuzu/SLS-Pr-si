// Renders one flyer HTML into A4 PDF, print PDF (3 mm bleed) and PNG preview.
// Usage: node render.js <flyer.html> <output prefix>
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const [html, prefix] = process.argv.slice(2).map(p => path.resolve(p));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 3 });
  await page.goto('file://' + html, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  await page.screenshot({ path: prefix + '_Vorschau.png' });
  await page.pdf({ path: prefix + '_A4.pdf', width: '210mm', height: '297mm', printBackground: true });

  await page.addStyleTag({ content: ':root{--b:3mm} @page{size:216mm 303mm}' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: prefix + '_Druck_3mm-Beschnitt.pdf', width: '216mm', height: '303mm', printBackground: true });

  await browser.close();
})();
