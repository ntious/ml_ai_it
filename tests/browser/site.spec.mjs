import { test, expect } from '@playwright/test';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const axePath = require.resolve('axe-core/axe.min.js');
const module3 = 'lessons/03-data-processing/index.html';

test('home connects learning paths, all modules, and the exact repository revision', async ({ page }) => {
  await page.goto('');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Learn machine learning. Build practical AI.');
  await expect(page.locator('.stage-grid a')).toHaveCount(14);
  await expect(page.getByRole('link', { name: 'GitHub repository' })).toHaveAttribute('href', /github\.com\/ntious\/ml_ai_it\/tree\/[0-9a-f]{40}$/);
  await page.keyboard.press('Tab');
  await expect(page.getByRole('link', { name: 'Skip to main content' })).toBeFocused();
  await page.keyboard.press('Enter');
  await expect(page.locator('#main')).toBeFocused();
  await page.getByRole('link', { name: 'Start with Module 1', exact: true }).click();
  await expect(page).toHaveURL(/lessons\/01-foundations\/index\.html$/);
});

test('module directory filters, reports empty results, and restores all modules', async ({ page }) => {
  await page.goto('modules.html');
  const query = page.getByRole('searchbox', { name: 'Find a module by topic' });
  await expect(query).toBeVisible();
  await expect(page.locator('[data-module-card]:visible')).toHaveCount(14);
  await query.fill('classification');
  await expect(page.locator('#module-count')).toHaveText('1 module shown.');
  await expect(page.locator('[data-module-card]:visible')).toHaveCount(1);
  await query.fill('a-topic-that-does-not-exist');
  await expect(page.locator('[data-module-empty]')).toBeVisible();
  await query.fill('');
  await expect(page.locator('[data-module-card]:visible')).toHaveCount(14);
});

test('lesson tabs and adjacent-module links preserve direct entry', async ({ page }) => {
  await page.goto(module3);
  const tabs = page.getByRole('navigation', { name: 'Module pages' });
  await expect(tabs.getByRole('link', { name: 'Overview', exact: true })).toHaveAttribute('aria-current', 'page');
  await tabs.getByRole('link', { name: 'Practice', exact: true }).click();
  await expect(page).toHaveURL(/03-data-processing\/practice\.html$/);
  await expect(page.getByRole('navigation', { name: 'Course outline' }).locator('[aria-current="location"]')).toContainText('Data processing');
  await page.getByRole('navigation', { name: 'Adjacent modules' }).getByRole('link', { name: /^Next: Module 4/ }).click();
  await expect(page).toHaveURL(/04-exploration\/index\.html$/);
});

test('mobile course outline uses a native disclosure and avoids page overflow', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto(module3);
  const outline = page.locator('[data-course-outline]');
  await expect(outline).not.toHaveAttribute('open', '');
  await outline.getByText('Course outline', { exact: true }).click();
  await expect(outline).toHaveAttribute('open', '');
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1)).toBeTruthy();
  await page.screenshot({ path: 'browser-results/module03-mobile.png', fullPage: true });
});

test('reading and module navigation remain usable without JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  try {
    await page.goto('http://127.0.0.1:4173/ml_ai_it/' + module3);
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
    await page.locator('summary').click();
    await expect(page.getByRole('navigation', { name: 'Course outline' })).toBeVisible();
    await page.getByRole('navigation', { name: 'Module pages' }).getByRole('link', { name: 'Foundation', exact: true }).click();
    await expect(page).toHaveURL(/03-data-processing\/foundation\.html$/);
    await page.goto('http://127.0.0.1:4173/ml_ai_it/modules.html');
    await expect(page.locator('[data-module-card]')).toHaveCount(14);
  } finally { await context.close(); }
});

test('local search finds concepts and handles zero results', async ({ page }) => {
  await page.goto('search.html?q=leakage');
  const query = page.getByRole('searchbox', { name: 'Search reading pages' });
  await expect(query).toBeVisible();
  await expect(page.locator('#search-results li').first()).toBeVisible();
  await query.fill('a-topic-that-does-not-exist');
  await query.press('Enter');
  await expect(page.locator('#search-status')).toContainText('No matching pages');
  await expect(page.locator('#search-results li')).toHaveCount(0);
  await expect(page).toHaveURL(/q=a-topic-that-does-not-exist/);
});

test('a deep missing URL offers a working project-prefix recovery route', async ({ page }) => {
  const response = await page.goto('missing/deep/page');
  expect(response.status()).toBe(404);
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('This page could not be found');
  await page.getByRole('link', { name: 'Return to the homepage', exact: true }).click();
  await expect(page).toHaveURL('http://127.0.0.1:4173/ml_ai_it/index.html');
});

test('representative pages reflow at three widths and enlarged text', async ({ page }) => {
  for (const width of [320, 768, 1440]) {
    await page.setViewportSize({ width, height: 1000 });
    for (const route of ['', 'modules.html', module3]) {
      await page.goto(route);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), route + ' at ' + width).toBeTruthy();
    }
  }
  await page.goto('');
  await page.addStyleTag({ content: 'html { font-size: 200%; }' });
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1)).toBeTruthy();
  await page.screenshot({ path: 'browser-results/home-large-text.png', fullPage: true });
  await page.goto('');
  await page.screenshot({ path: 'browser-results/home-desktop.png', fullPage: true });
});

test('representative light and dark pages have no detected axe WCAG A/AA violations', async ({ page }) => {
  for (const colorScheme of ['light', 'dark']) {
    await page.emulateMedia({ colorScheme });
    for (const route of ['', 'modules.html', module3, 'search.html', 'downloads.html', 'instructor/index.html']) {
      await page.goto(route);
      await page.addScriptTag({ path: axePath });
      const result = await page.evaluate(async () => window.axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] } }));
      expect(result.violations.map(item => ({ id: item.id, impact: item.impact, nodes: item.nodes.map(node => node.target) })), route + ' / ' + colorScheme).toEqual([]);
    }
  }
});
