// Build trusted repository Markdown into a static reading site.
// Optional search/disclosure enhancements never replace the reading content.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';
import { moduleDirectory, learningStages, notebookDownloads, courseOutline, moduleTabs, modulePager } from './site_components.mjs';

const require = createRequire(import.meta.url);
const { marked } = await import(pathToFileURL(require.resolve('marked')).href);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const site = path.join(root, 'site');
const slash = value => value.split(path.sep).join('/');
const escape = value => value.replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
function walk(folder) {
  return fs.readdirSync(folder, { withFileTypes: true }).flatMap(entry => entry.isDirectory()
    ? walk(path.join(folder, entry.name)) : [path.join(folder, entry.name)]);
}
const modules = JSON.parse(fs.readFileSync(path.join(root, 'curriculum/modules.json'), 'utf8')).modules;
const config = JSON.parse(fs.readFileSync(path.join(root, 'curriculum/site.json'), 'utf8'));
const sourceRef = process.env.SITE_SOURCE_REF || (() => {
  try { return execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim(); }
  catch { return 'development/module-03-foundation'; }
})();
if (!/^[a-zA-Z0-9._/-]+$/.test(sourceRef)) throw new Error('Invalid source ref.');
const basePath = process.env.SITE_BASE_PATH || config.base_path;
if (!/^\/(?:[a-zA-Z0-9_-]+\/)*$/.test(basePath)) throw new Error('Use a slash-delimited site base path.');
const searchEntries = [];
const lessonURLForFirst = () => modules[0].lesson.replace(/^docs\//, '').replace(/\.md$/, '.html');
const pages = walk(path.join(root, 'docs')).filter(p => p.endsWith('.md')).map(source => ({
  source, output: path.relative(path.join(root, 'docs'), source).replace(/\.md$/, '.html')
}));
pages.push({ source: path.join(root, 'QUICKSTART.md'), output: 'setup/quickstart.html' });
pages.push({ source: path.join(root, 'ACCESSIBILITY.md'), output: 'accessibility/policy.html' });
pages.push({ source: path.join(root, 'REPOSITORY_STRUCTURE.md'), output: 'maintenance/architecture.html' });
pages.push({ source: path.join(root, 'REPOSITORY_REVIEW.md'), output: 'maintenance/review.html' });
for (const name of ['README', 'DEVELOPMENT', 'CONTRIBUTING', 'CHANGELOG', 'OER_LICENSE', 'CODE_OF_CONDUCT']) {
  pages.push({ source: path.join(root, name + '.md'), output: 'maintenance/' + name.toLowerCase() + '.html' });
}
for (const source of walk(path.join(root, 'templates')).filter(p => p.endsWith('.md'))) {
  pages.push({ source, output: 'authoring/' + path.basename(source).replace(/\.md$/, '.html') });
}
const mapping = new Map(pages.map(p => [p.source, p.output]));
// A fixed generated-only directory: remove stale pages before rebuilding.
fs.rmSync(site, { recursive: true, force: true });
fs.mkdirSync(site, { recursive: true });
for (const page of pages) {
  const markdown = fs.readFileSync(page.source, 'utf8');
  const title = markdown.match(/^# (.+)$/m)?.[1];
  if (!title) throw new Error(`Missing page title: ${page.source}`);
  const relative = target => slash(path.relative(path.dirname(page.output), target)) || 'index.html';
  const module = modules.find(item => page.source.startsWith(path.join(root, 'docs/lessons', item.slug) + path.sep));
  const usedIds = new Map();
  let body = marked.parse(markdown, { gfm: true });
  // Overflowing examples need an explicit keyboard-focus target.
  body = body.replaceAll('<pre>', '<pre tabindex="0" aria-label="Code or text example">');
  body = body.replace(/<h([1-6])>([\s\S]*?)<\/h\1>/g, (_, level, text) => {
    const base = text.replace(/<[^>]+>/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    const count = usedIds.get(base) || 0; usedIds.set(base, count + 1);
    return `<h${level} id="${base}${count ? `-${count}` : ''}">${text}</h${level}>`;
  });
  let tableNumber = 0;
  body = body.replace(/<table>([\s\S]*?)<\/table>/g, (table, contents, offset) => {
    const headings = [...body.slice(0, offset).matchAll(/<h[1-6][^>]*>([\s\S]*?)<\/h[1-6]>/g)];
    const context = (headings.at(-1)?.[1] || title).replace(/<[^>]+>/g, '');
    const caption = escape(context + ' — table ' + (++tableNumber));
    const scoped = contents.replace(/<th>/g, '<th scope="col">');
    return '<div class="table-wrap" tabindex="0" role="region" aria-label="' + caption + '"><table><caption>' + caption + '</caption>' + scoped + '</table></div>';
  });
  body = body.replace(/href="([^"]+)"/g, (original, href) => {
    if (/^(https?:|mailto:|#)/.test(href)) return original;
    const [target, fragment] = href.split('#');
    if (target === 'LICENSE') return 'href="' + slash(path.relative(path.dirname(page.output), 'maintenance/license.txt')) + '"';
    if (!target.endsWith('.md')) return original;
    const mapped = mapping.get(path.resolve(path.dirname(page.source), target));
    if (!mapped) throw new Error(`Unmapped Markdown link: ${href} in ${page.source}`);
    return `href="${slash(path.relative(path.dirname(page.output), mapped))}${fragment ? `#${fragment}` : ''}"`;
  });
  // Markers keep the Markdown fallback useful on GitHub while rendering the
  // directory from the same registry used by scripts and downloads.
  body = body.replace(/<!-- MODULE_DIRECTORY_START -->[\s\S]*?<!-- MODULE_DIRECTORY_END -->/g, moduleDirectory(modules, relative));
  body = body.replace('<!-- LEARNING_STAGES -->', learningStages(modules, relative));
  body = body.replace('<!-- NOTEBOOK_DOWNLOADS -->', notebookDownloads(modules, relative));
  body = body.replace('<!-- HOME_ACTIONS -->', '<div class="hero-actions"><a class="button button-primary" href="' + relative(lessonURLForFirst()) + '">Start with Module 1</a><a class="button button-secondary" href="' + relative('modules.html') + '">Explore all modules</a><a class="text-action" href="' + config.repository + '/tree/' + sourceRef + '">View on GitHub <span aria-hidden="true">↗</span></a></div>');
  const navigation = [
    ['modules.html', 'Modules'], ['examples.html', 'Examples'], ['downloads.html', 'Downloads'],
    ['instructor/index.html', 'Teach'], ['setup/index.html', 'Get started'], ['search.html', 'Search']
  ].map(([url, label]) => '<li><a href="' + relative(url) + '"' + (url === page.output ? ' aria-current="page"' : '') + '>' + label + '</a></li>').join('');
  const sourcePath = slash(path.relative(root, page.source));
  const sourceURL = config.repository + '/blob/' + sourceRef + '/' + sourcePath;
  const plainText = body.replace(/<pre[\s\S]*?<\/pre>/g, ' ').replace(/<[^>]+>/g, ' ').replace(/&[a-z#0-9]+;/gi, ' ').replace(/\s+/g, ' ').trim();
  if (page.output !== '404.html' && page.output !== 'search.html') {
    searchEntries.push({ title, url: page.output, summary: plainText.slice(0, 220), text: plainText.slice(0, 16000) });
  }
  const html = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">' +
    (page.output === '404.html' ? '<base href="' + basePath + '">' : '') +
    '<meta name="description" content="' + escape(page.output === 'index.html' ? config.description : plainText.slice(0, 170)) + '">' +
    '<meta name="color-scheme" content="light dark"><title>' + escape(title) + ' | Practical ML &amp; AI</title>' +
    '<link rel="icon" href="' + relative('assets/favicon.svg') + '" type="image/svg+xml">' +
    '<link rel="stylesheet" href="' + relative('assets/site.css') + '">' +
    '<script type="module" src="' + relative('assets/site.js') + '"></script></head>' +
    '<body class="' + (page.output === 'index.html' ? 'home-page' : 'reading-page') + '" data-search-index="' + relative('search-index.json') + '">' +
    '<a class="skip-link" href="#main">Skip to main content</a>' +
    '<header class="site-header"><a class="brand" href="' + relative('index.html') + '"><span class="brand-mark" aria-hidden="true">ML</span><span>Practical ML <span class="brand-amp">&amp;</span> AI</span></a>' +
    '<nav aria-label="Main navigation"><ul>' + navigation + '</ul></nav><a class="repo-link" href="' + config.repository + '/tree/' + sourceRef + '">GitHub repository <span aria-hidden="true">↗</span></a></header>' +
    '<div class="site-layout' + (module ? ' lesson-layout' : '') + '">' +
    (module ? courseOutline(modules, module, relative) : '') +
    '<main id="main" tabindex="-1">' +
    (module ? '<p class="eyebrow">Module ' + module.id + ' · ' + escape(module.track) + '</p>' + moduleTabs(module, page.output, relative) : '') +
    body +
    (module ? modulePager(modules, module, relative) : '') +
    '<div class="page-source"><a href="' + escape(sourceURL) + '">View source for this page on GitHub</a></div></main></div>' +
    '<footer class="site-footer"><div><a class="footer-title" href="' + relative('index.html') + '">Practical Machine Learning and AI Systems</a><p>Build understanding. Inspect evidence. Explain the limits.</p><p>' + escape(config.edition) + ' · Independent learning and adaptable teaching.</p></div>' +
    '<nav aria-label="Resource links"><ul><li><a href="' + relative('accessibility/index.html') + '">Accessibility and support</a></li><li><a href="' + relative('data-sources.html') + '">Data and model sources</a></li><li><a href="' + relative('ai-collaboration.html') + '">Learning with GenAI</a></li><li><a href="' + config.repository + '">Repository home</a></li><li><a href="' + relative('maintenance/oer_license.html') + '">Reuse and licensing</a></li></ul></nav><p class="license-note">Original code: MIT. Original educational content: CC BY 4.0. External sources retain their own terms.</p></footer></body></html>\n';
  const destination = path.join(site, page.output);
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, html);
}
fs.mkdirSync(path.join(site, 'assets'), { recursive: true });
for (const name of ['site.css', 'site.js', 'favicon.svg']) {
  fs.copyFileSync(path.join(root, 'docs/assets', name), path.join(site, 'assets', name));
}
fs.writeFileSync(path.join(site, 'search-index.json'), JSON.stringify(searchEntries));
fs.writeFileSync(path.join(site, 'site-build.json'), JSON.stringify({
  repository: config.repository, source_ref: sourceRef,
  workflow_run_id: process.env.GITHUB_RUN_ID || null, modules: modules.length,
  reading_pages: pages.length, base_path: basePath
}, null, 2) + '\n');
fs.writeFileSync(path.join(site, '.nojekyll'), '');

fs.copyFileSync(path.join(root, 'LICENSE'), path.join(site, 'maintenance/license.txt'));
execFileSync(process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3'), [path.join(root, 'scripts/build_downloads.py')], { cwd: root, stdio: 'inherit' });
console.log(`Built ${pages.length} reading pages. No deployment performed.`);
