// Semantic components for the static course site. No runtime framework needed.
export const escape = value => String(value).replaceAll('&', '&amp;').replaceAll('"', '&quot;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
export const lessonURL = module => module.lesson.replace(/^docs\//, '').replace(/\.md$/, '.html');
const link = (href, text, className = '') => '<a' + (className ? ' class="' + className + '"' : '') + ' href="' + escape(href) + '">' + escape(text) + '</a>';

export function moduleDirectory(modules, relative) {
  return '<section aria-labelledby="module-directory"><h2 id="module-directory">Choose a module</h2><div class="directory-tools" data-module-tools hidden><label for="module-query">Find a module by topic</label><input id="module-query" type="search" autocomplete="off" placeholder="Try Python, evaluation, or language"><p id="module-count" role="status" aria-live="polite"></p></div>' +
    '<div class="module-grid" data-module-grid>' + modules.map(module =>
      '<article class="module-card" data-module-card data-search="' + escape([module.id, module.title, module.track, module.summary].join(' ').toLowerCase()) + '">' +
      '<p class="eyebrow">Module ' + module.id + ' · ' + escape(module.track) + '</p><h3>' + link(relative(lessonURL(module)), module.title) +
      '</h3><p>' + escape(module.summary) + '</p><p class="environment-label">' + (module.profile === 'core' ? 'Core Python environment' : 'Framework environment') + '</p></article>'
    ).join('') + '</div><p data-module-empty hidden>No matching modules. Try a broader topic or clear the search.</p></section>';
}

export function learningStages(modules, relative) {
  const tracks = [...new Set(modules.map(module => module.track))];
  return '<ol class="stage-grid">' + tracks.map((track, index) =>
    '<li><p class="eyebrow">Stage ' + (index + 1) + '</p><h3>' + escape(track) + '</h3><ul>' +
    modules.filter(module => module.track === track).map(module => '<li>' + link(relative(lessonURL(module)), module.id + '. ' + module.title) + '</li>').join('') + '</ul></li>'
  ).join('') + '</ol>';
}

export function notebookDownloads(modules, relative) {
  return '<div class="table-wrap" tabindex="0" role="region" aria-label="Notebook downloads"><table><caption>Clean source and executed notebook copies by module</caption><thead><tr><th scope="col">Module</th><th scope="col">Start fresh</th><th scope="col">Inspect saved outputs</th></tr></thead><tbody>' +
    modules.map(module => '<tr><th scope="row">' + escape(module.id + '. ' + module.title) + '</th><td>' +
      link(relative('downloads/' + module.download), 'Source notebook, module ' + module.id) + '</td><td>' +
      link(relative('downloads/' + module.download.replace(/[^/]+$/, 'executed.ipynb')), 'Executed notebook, module ' + module.id) + '</td></tr>').join('') +
    '</tbody></table></div>';
}

export function courseOutline(modules, current, relative) {
  return '<aside class="course-sidebar"><details class="course-outline" data-course-outline><summary>Course outline</summary><nav aria-label="Course outline"><ol>' +
    modules.map(module => '<li><a href="' + escape(relative(lessonURL(module))) + '" data-progress-module="' + escape(lessonURL(module).replace(/index\.html$/, '')) + '"' +
      (current?.id === module.id ? ' aria-current="location" class="current-module"' : '') +
      '><span class="module-number" aria-hidden="true">' + String(module.id).padStart(2, '0') + '</span><span><span class="visually-hidden">Module ' + module.id + ': </span>' + escape(module.title) + '</span><span class="outline-progress" data-progress-count hidden></span></a></li>').join('') +
    '</ol></nav></details><p class="sidebar-help">' + link(relative('setup/index.html'), 'Setup and troubleshooting') + '<br>' + link(relative('accessibility/index.html'), 'Access routes and support') + '</p></aside>';
}

export function moduleTabs(module, output, relative) {
  // Short labels keep all eight pages on one row at desktop widths.
  const labels = {'concepts.md': 'Concepts', 'solutions.md': 'Solutions', 'guided.md': 'Guided', 'index.md': 'Overview', 'foundation.md': 'Foundation', 'practice.md': 'Practice', 'feedback.md': 'Feedback', 'instructor.md': 'Teaching notes'};
  return '<nav class="lesson-tabs" aria-label="Module pages"><ul>' + module.pages.map(name => {
    const target = module.lesson.replace(/index\.md$/, name).replace(/^docs\//, '').replace(/\.md$/, '.html');
    return '<li><a href="' + escape(relative(target)) + '" data-progress-page="' + escape(target) + '"' + (output === target ? ' aria-current="page"' : '') + '>' + labels[name] + '</a></li>';
  }).join('') + '</ul></nav>';
}

export function modulePager(modules, current, relative) {
  const previous = modules.find(module => module.id === current.id - 1);
  const next = modules.find(module => module.id === current.id + 1);
  return '<nav class="module-pager" aria-label="Adjacent modules">' +
    (previous ? link(relative(lessonURL(previous)), 'Previous: Module ' + previous.id + ' — ' + previous.title) : '<span></span>') +
    (next ? link(relative(lessonURL(next)), 'Next: Module ' + next.id + ' — ' + next.title) : link(relative('examples.html'), 'Continue with worked examples')) +
    '</nav>';
}

// Original diagram of the evaluation loop the course teaches; colours follow the site theme.
export function heroFigure() {
  const steps = [['1', 'Decide', 'task, user and error costs'], ['2', 'Baseline', 'a simple method first'],
                 ['3', 'Validate', 'choose on development data'], ['4', 'Test once', 'report the locked choice']];
  const cards = steps.map(([number, title, note], index) => {
    const y = 18 + index * 74;
    return '<g class="hero-step" transform="translate(0 ' + y + ')"><rect x="22" y="0" width="300" height="58" rx="12"/>' +
      '<circle class="hero-badge" cx="54" cy="29" r="15"/><text class="hero-number" x="54" y="34" text-anchor="middle">' + number + '</text>' +
      '<text class="hero-title" x="84" y="25">' + title + '</text><text class="hero-note" x="84" y="45">' + note + '</text></g>' +
      (index < steps.length - 1 ? '<path class="hero-arrow" d="M172 ' + (y + 60) + 'v12"/>' : '');
  }).join('');
  return '<figure class="hero-figure"><svg viewBox="0 0 344 330" role="img" aria-labelledby="hero-figure-title hero-figure-desc">' +
    '<title id="hero-figure-title">How every result in the course is checked</title>' +
    '<desc id="hero-figure-desc">Four steps: decide the task and error costs, try a simple baseline first, choose settings on development data, then test the locked choice once. Poor results stay visible.</desc>' +
    cards + '<text class="hero-foot" x="172" y="322" text-anchor="middle">Poor results stay visible.</text></svg></figure>';
}
