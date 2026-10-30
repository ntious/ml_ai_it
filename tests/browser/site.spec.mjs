import { test, expect } from '@playwright/test';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const axePath = require.resolve('axe-core/axe.min.js');
const module3 = 'lessons/03-data-processing/index.html';

test('prototype practice hints work by keyboard and solutions stay a separate page', async ({ page }) => {
  await page.setViewportSize({ width: 320, height: 900 });
  for (const slug of ['05-regression', '06-classification', '08-neural-networks']) {
    await page.goto(`lessons/${slug}/practice.html`);
    const hint = page.locator('main details').first();
    await expect(hint).toHaveJSProperty('open', false);
    await hint.locator('summary').focus();
    await page.keyboard.press('Enter');
    await expect(hint).toHaveJSProperty('open', true);
    await page.locator('main a[href="solutions.html"]').last().click();
    await expect(page).toHaveURL(new RegExp(`${slug}/solutions.html$`));
    await expect(page.getByRole('heading', { level: 1 })).toContainText('practice solutions');
  }
});

test('home connects learning paths, all modules, and the main repository', async ({ page }) => {
  await page.goto('');
  await expect(page.getByRole('heading', { level: 1 })).toHaveText('Learn machine learning. Build practical AI.');
  await expect(page.locator('.stage-grid a')).toHaveCount(14);
  await expect(page.getByRole('link', { name: /Course repository/ })).toHaveAttribute('href', /github\.com\/ntious\/ml_ai_it\/tree\/main$/);
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

test('narrow screens get a compact menu that opens, closes with Escape and keeps content first', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('index.html');
  const menu = page.getByRole('button', { name: 'Menu' });
  const nav = page.getByRole('navigation', { name: 'Main navigation' });
  await expect(menu).toHaveAttribute('aria-expanded', 'false');
  await expect(nav).toBeHidden();
  expect(await page.locator('[data-site-header]').evaluate(element => element.getBoundingClientRect().height)).toBeLessThan(110);
  await menu.click();
  await expect(menu).toHaveAttribute('aria-expanded', 'true');
  await expect(nav.getByRole('link', { name: 'Modules' })).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(nav).toBeHidden();
  await expect(menu).toBeFocused();
  await page.setViewportSize({ width: 1366, height: 900 });
  await expect(menu).toBeHidden();
  await expect(nav).toBeVisible();
});

test('search ranks relevant pages first and highlights matches', async ({ page }) => {
  await page.goto('search.html?q=threshold');
  const first = page.locator('#search-results li').first();
  await expect(first.getByRole('link')).toContainText('Module 6');
  await expect(first.locator('mark').first()).toHaveText(/threshold/i);
  await expect(page.locator('#search-status')).toContainText('most relevant first');
});

test('lesson tabs stay on one row and progress marks persist in this browser', async ({ page }) => {
  await page.setViewportSize({ width: 1366, height: 900 });
  await page.goto('lessons/06-classification/concepts.html');
  const tops = await page.locator('.lesson-tabs li').evaluateAll(items => new Set(items.map(item => item.offsetTop)).size);
  expect(tops).toBe(1);
  // The row is not scrolled away from the first tab, and the current tab is fully visible.
  expect(await page.locator('.lesson-tabs ul').evaluate(list => {
    const current = list.querySelector('[aria-current="page"]').getBoundingClientRect();
    const row = list.getBoundingClientRect();
    return [list.scrollLeft, current.left >= row.left && current.right <= row.right];
  })).toEqual([0, true]);
  await expect(page.locator('.page-progress')).toContainText('Page 3 of 8');
  const mark = page.getByRole('button', { name: 'Mark this page complete' });
  await mark.click();
  await expect(page.getByRole('button', { name: /Completed/ })).toHaveAttribute('aria-pressed', 'true');
  await page.reload();
  await expect(page.getByRole('button', { name: /Completed/ })).toHaveAttribute('aria-pressed', 'true');
  await expect(page.locator('.lesson-tabs a.is-done')).toHaveCount(1);
  await expect(page.locator('[data-progress-module="lessons/06-classification/"] [data-progress-count]')).toHaveText('1 done');
});

test('self-checks invite an answer first, and reduced motion removes transitions', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('lessons/06-classification/concepts.html');
  await expect(page.getByRole('textbox', { name: /Your answer to question \d/ })).toHaveCount(3);
  expect(await page.locator('main details').first().evaluate(element => getComputedStyle(element).transitionDuration)).toBe('0s');
  await page.goto('index.html');
  await expect(page.getByRole('img', { name: 'How every result in the course is checked' })).toBeVisible();
});

test('on a phone, the current lesson tab is scrolled into view', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('lessons/06-classification/feedback.html');
  expect(await page.locator('.lesson-tabs ul').evaluate(list => {
    const current = list.querySelector('[aria-current="page"]').getBoundingClientRect();
    const row = list.getBoundingClientRect();
    return current.left >= row.left - 1 && current.right <= row.right + 1;
  })).toBe(true);
});

test('theme overrides system, persists across pages, and returns to system', async ({ page }) => {
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto('');
  const theme = page.getByRole('combobox', { name: 'Color theme' });
  await expect(theme).toHaveValue('system');
  await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(17, 30, 37)');
  await theme.selectOption('light');
  await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(248, 250, 247)');
  await page.goto(module3);
  await expect(page.getByRole('combobox', { name: 'Color theme' })).toHaveValue('light');
  await page.getByRole('combobox', { name: 'Color theme' }).selectOption('dark');
  await page.emulateMedia({ colorScheme: 'light' });
  await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(17, 30, 37)');
  await page.getByRole('combobox', { name: 'Color theme' }).selectOption('system');
  await expect(page.locator('body')).toHaveCSS('background-color', 'rgb(248, 250, 247)');
  await page.setViewportSize({ width: 320, height: 900 });
  await page.getByRole('button', { name: 'Menu' }).click();
  await expect(page.getByRole('combobox', { name: 'Color theme' })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});

test('repository counts are cached and failed requests leave a usable link', async ({ page }) => {
  let requests = 0;
  await page.route('https://api.github.com/repos/ntious/ml_ai_it', route => {
    requests++;
    return route.fulfill({ json: { stargazers_count: 12, forks_count: 3 } });
  });
  await page.goto('');
  await expect(page.locator('[data-repo-stats]')).toHaveText('★ 12 stars · 3 forks');
  await page.goto(module3);
  await expect(page.locator('[data-repo-stats]')).toHaveText('★ 12 stars · 3 forks');
  expect(requests).toBe(1);
  await page.evaluate(() => sessionStorage.clear());
  await page.unroute('https://api.github.com/repos/ntious/ml_ai_it');
  await page.route('https://api.github.com/repos/ntious/ml_ai_it', route => route.fulfill({ status: 403, body: '{}' }));
  await page.reload();
  await expect(page.locator('[data-repo-stats]')).toBeHidden();
  await expect(page.locator('.repo-link')).toHaveAttribute('href', 'https://github.com/ntious/ml_ai_it/tree/main');
});
