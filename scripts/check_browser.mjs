// Reproducible reading-site checks. Human/assistive-technology use is separate.
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';
import fs from 'node:fs/promises';
import path from 'node:path';
import http from 'node:http';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const output = path.join(root, 'runs/browser-review');
await fs.mkdir(output, { recursive: true });
const site = path.join(root, 'site');
const server = http.createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    let target = path.resolve(site, '.' + pathname);
    if (target !== site && !target.startsWith(site + path.sep)) throw new Error('Outside site');
    if ((await fs.stat(target)).isDirectory()) target = path.join(target, 'index.html');
    const content = await fs.readFile(target);
    response.writeHead(200, { 'Content-Type': target.endsWith('.css') ? 'text/css' : 'text/html; charset=utf-8' });
    response.end(content);
  } catch { response.writeHead(404); response.end('Not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const base = 'http://127.0.0.1:' + server.address().port + '/';
let browser;
try {
  browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await context.newPage();
  const results = [];
  for (const route of ['overview.html', 'start-here.html', 'setup/python-bridge.html', 'lessons/08-neural-networks/guided.html', 'cases/phishing.html',
    'projects/phishing-triage/index.html', 'projects/phishing-triage/reports/annotated-report.html',
    'advanced/index.html', 'advanced/tuning.html', 'advanced/stability.html', 'advanced/evaluation.html']) {
    const response = await page.goto(base + route);
    if (!response.ok()) throw new Error('Reading page unavailable: ' + route);
    await page.bringToFront();
    await page.keyboard.press('Tab');
    const firstHref = await page.evaluate(() => document.activeElement?.getAttribute('href'));
    if (firstHref !== '#main') throw new Error('Skip link is not first: ' + route + ' focus=' + firstHref);
    await page.keyboard.press('Enter');
    if (await page.locator(':focus').getAttribute('id') !== 'main') throw new Error('Skip link did not move focus: ' + route);
    const scan = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
    if (scan.violations.length) throw new Error(JSON.stringify(scan.violations.map(issue => ({ id: issue.id, elements: issue.nodes.length }))));
    await page.setViewportSize({ width: 320, height: 900 });
    const widths = await page.evaluate(() => ({ document: document.documentElement.scrollWidth, viewport: innerWidth }));
    if (widths.document > widths.viewport + 1) throw new Error('Page-level overflow: ' + route + ' ' + JSON.stringify(widths));
    results.push({ route, axeViolations: scan.violations.length, skipFocus: true, widths });
    if (route === 'overview.html') await page.screenshot({ path: path.join(output, 'readme-mobile.png') });
    if (route === 'start-here.html') await page.screenshot({ path: path.join(output, 'start-mobile.png') });
    if (route === 'projects/phishing-triage/reports/annotated-report.html') await page.screenshot({ path: path.join(output, 'capstone-report-mobile.png') });
    await page.setViewportSize({ width: 1280, height: 900 });
    if (route === 'lessons/08-neural-networks/guided.html') {
      await page.locator('main').scrollIntoViewIfNeeded();
      await page.screenshot({ path: path.join(output, 'guided-desktop.png') });
    }
    if (route === 'projects/phishing-triage/index.html') await page.screenshot({ path: path.join(output, 'capstone-desktop.png') });
  }
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto(base + 'start-here.html');
  const dark = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21aa']).analyze();
  if (dark.violations.length) throw new Error('Dark-mode accessibility-rule violations.');
  const report = { browser: browser.version(), results, darkViolations: dark.violations.length,
    limits: `${results.length} reading pages and selected automated rules; no screen-reader, human keyboard, real zoom or hosted notebook/app interface claim.` };
  await fs.writeFile(path.join(output, 'checks.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
} finally {
  if (browser) await browser.close();
  await new Promise(resolve => server.close(resolve));
}
