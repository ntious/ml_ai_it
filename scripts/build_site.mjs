// Build trusted repository Markdown into a semantic, JavaScript-free reading site.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { execFileSync } from 'node:child_process';

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
const pages = walk(path.join(root, 'docs')).filter(p => p.endsWith('.md')).map(source => ({
  source, output: path.relative(path.join(root, 'docs'), source).replace(/\.md$/, '.html')
}));
pages.push({ source: path.join(root, 'QUICKSTART.md'), output: 'setup/quickstart.html' });
pages.push({ source: path.join(root, 'ACCESSIBILITY.md'), output: 'accessibility/policy.html' });
pages.push({ source: path.join(root, 'REPOSITORY_STRUCTURE.md'), output: 'maintenance/architecture.html' });
pages.push({ source: path.join(root, 'README.md'), output: 'overview.html' });
for (const name of ['DEVELOPMENT', 'CONTRIBUTING', 'CHANGELOG', 'OER_LICENSE', 'CODE_OF_CONDUCT']) {
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
  const usedIds = new Map();
  let body = marked.parse(markdown, { gfm: true });
  // Source links use the published GitHub Pages URL. In the built site their
  // explicit Markdown title selects the actual local download instead.
  body = body.replace(/<a href="[^"]+" title="site-download:([^"]+)">/g, (_, name) => {
    const destination = path.resolve(site, 'downloads', name);
    if (!destination.startsWith(path.join(site, 'downloads') + path.sep)) throw new Error('Escaping download');
    return '<a href="' + slash(path.relative(path.dirname(page.output), 'downloads/' + name)) + '">';
  });
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
    if (href === 'https://github.com/ntious/ml_ai_it/blob/main/notebooks/cases/phishing.ipynb') return 'href="' + slash(path.relative(path.dirname(page.output), 'downloads/phishing/walkthrough.ipynb')) + '"';
    if (/^(https?:|mailto:|#)/.test(href)) return original;
    const [target, fragment] = href.split('#');
    if (target === 'CITATION.cff') return 'href="' + slash(path.relative(path.dirname(page.output), 'maintenance/citation.cff')) + '"';
    if (target === 'LICENSE') return 'href="' + slash(path.relative(path.dirname(page.output), 'maintenance/license.txt')) + '"';
    if (!target.endsWith('.md')) return original;
    const mapped = mapping.get(path.resolve(path.dirname(page.source), target));
    if (!mapped) throw new Error(`Unmapped Markdown link: ${href} in ${page.source}`);
    return `href="${slash(path.relative(path.dirname(page.output), mapped))}${fragment ? `#${fragment}` : ''}"`;
  });
  const relative = target => slash(path.relative(path.dirname(page.output), target)) || 'index.html';
  const navigation = [
    ['index.html', 'Home'], ['overview.html', 'Course overview'], ['start-here.html', 'Start here'], ['glossary.html', 'Glossary'], ['project.html', 'Project'],
    ...modules.map(module => [module.lesson.replace(/^docs\//, '').replace(/\.md$/, '.html'), 'Module ' + module.id]),
    ['setup/index.html', 'Setup'], ['accessibility/index.html', 'Accessibility'],
    ['instructor/index.html', 'Teach and adapt']
  ].map(([url, label]) => `<li><a href="${relative(url)}"${url === page.output ? ' aria-current="page"' : ''}>${label}</a></li>`).join('');
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escape(title)} | Practical ML and AI</title><link rel="stylesheet" href="${relative('assets/site.css')}"></head>
<body><a class="skip-link" href="#main">Skip to main content</a>
<header><p>Practical Machine Learning and AI Systems · Learning companion</p><nav aria-label="Main navigation"><ul>${navigation}</ul></nav></header>
<main id="main" tabindex="-1">${body}</main>
<footer><p>Original code: MIT. Original educational content: CC BY 4.0. <a href="${relative('accessibility/index.html')}">Accessibility status and limitations</a>.</p></footer>
</body></html>\n`;
  const destination = path.join(site, page.output);
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, html);
}
fs.mkdirSync(path.join(site, 'assets'), { recursive: true });
fs.copyFileSync(path.join(root, 'docs/assets/site.css'), path.join(site, 'assets/site.css'));
fs.copyFileSync(path.join(root, 'LICENSE'), path.join(site, 'maintenance/license.txt'));
fs.copyFileSync(path.join(root, 'CITATION.cff'), path.join(site, 'maintenance/citation.cff'));
execFileSync(process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3'), [path.join(root, 'scripts/build_downloads.py')], { cwd: root, stdio: 'inherit' });
console.log(`Built ${pages.length} reading pages. No deployment performed.`);
