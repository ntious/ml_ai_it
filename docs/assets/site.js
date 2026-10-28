// Optional enhancements. Reading, module links, menus and native disclosures still
// work without JavaScript. Search stays in this browser; no query is sent away.
const narrow = window.matchMedia('(max-width: 63.99rem)');

const outline = document.querySelector('[data-course-outline]');
if (outline && !narrow.matches) outline.open = true;

// Compact menu on narrow screens. Without JavaScript the full menu stays visible.
const header = document.querySelector('[data-site-header]');
const menuButton = header?.querySelector('.menu-toggle');
if (header && menuButton) {
  const setMenu = open => {
    header.dataset.menu = open ? 'open' : 'closed';
    menuButton.setAttribute('aria-expanded', String(open));
  };
  const fitMenu = () => {
    menuButton.hidden = !narrow.matches;
    if (narrow.matches) setMenu(false);
    else { delete header.dataset.menu; menuButton.setAttribute('aria-expanded', 'false'); }
  };
  menuButton.addEventListener('click', () => setMenu(header.dataset.menu !== 'open'));
  header.addEventListener('keydown', event => {
    if (event.key === 'Escape' && header.dataset.menu === 'open') { setMenu(false); menuButton.focus(); }
  });
  narrow.addEventListener('change', fitMenu);
  fitMenu();
}

// Keep the current lesson tab visible in the single scrolling row; scroll only if it is cut off.
const tabList = document.querySelector('.lesson-tabs ul');
const currentTab = tabList?.querySelector('[aria-current="page"]')?.parentElement;
if (tabList && currentTab) {
  const overflow = currentTab.getBoundingClientRect().right - tabList.getBoundingClientRect().right;
  if (overflow > 0) tabList.scrollLeft += overflow + 16;
}

// Progress marks are stored only in this browser. If storage is blocked, the feature stays off.
const PROGRESS_KEY = 'ml-ai-it-progress-v1';
const readProgress = () => {
  try { return new Set(JSON.parse(localStorage.getItem(PROGRESS_KEY) || '[]')); } catch { return null; }
};
const writeProgress = done => {
  try { localStorage.setItem(PROGRESS_KEY, JSON.stringify([...done])); return true; } catch { return false; }
};
const progress = readProgress();
if (progress) {
  const tabs = [...document.querySelectorAll('.lesson-tabs [data-progress-page]')];
  const showProgress = () => {
    for (const tab of tabs) {
      const done = progress.has(tab.dataset.progressPage);
      tab.classList.toggle('is-done', done);
      let note = tab.querySelector('.visually-hidden');
      if (done && !note) { note = document.createElement('span'); note.className = 'visually-hidden'; note.textContent = ' (completed)'; tab.append(note); }
      if (!done && note) note.remove();
    }
    for (const link of document.querySelectorAll('[data-progress-module]')) {
      const count = [...progress].filter(page => page.startsWith(link.dataset.progressModule)).length;
      const badge = link.querySelector('[data-progress-count]');
      badge.hidden = count === 0;
      badge.textContent = count ? count + ' done' : '';
    }
  };
  const current = tabs.find(tab => tab.getAttribute('aria-current') === 'page');
  if (current) {
    const bar = document.createElement('div');
    bar.className = 'page-progress';
    const position = document.createElement('span');
    position.textContent = 'Page ' + (tabs.indexOf(current) + 1) + ' of ' + tabs.length;
    const mark = document.createElement('button');
    mark.type = 'button';
    mark.className = 'progress-mark';
    const label = () => {
      const done = progress.has(current.dataset.progressPage);
      mark.setAttribute('aria-pressed', String(done));
      mark.textContent = done ? '✓ Completed' : 'Mark this page complete';
    };
    mark.addEventListener('click', () => {
      const page = current.dataset.progressPage;
      progress.has(page) ? progress.delete(page) : progress.add(page);
      if (writeProgress(progress)) { label(); showProgress(); }
    });
    const privacy = document.createElement('span');
    privacy.className = 'progress-note';
    privacy.textContent = 'Saved in this browser only.';
    label();
    bar.append(position, mark, privacy);
    current.closest('.lesson-tabs').after(bar);
  }
  showProgress();
}

// Invite an answer before each self-check explanation is opened; nothing is saved or sent.
for (const heading of document.querySelectorAll('main h2')) {
  if (heading.textContent.trim() !== 'Check yourself') continue;
  let number = 0;
  for (let node = heading.nextElementSibling; node && node.tagName !== 'H2'; node = node.nextElementSibling) {
    if (node.tagName !== 'DETAILS') continue;
    number++;
    const field = document.createElement('div');
    field.className = 'self-check-answer';
    const label = document.createElement('label');
    const id = 'self-check-' + number;
    label.htmlFor = id;
    label.textContent = 'Your answer to question ' + number + ' (not saved)';
    const box = document.createElement('textarea');
    box.id = id;
    box.rows = 2;
    field.append(label, box);
    // After the question card: read the question, write an answer, then open the card to compare.
    node.after(field);
  }
}

const tools = document.querySelector('[data-module-tools]');
if (tools) {
  const input = tools.querySelector('input');
  const cards = [...document.querySelectorAll('[data-module-card]')];
  const count = document.querySelector('#module-count');
  const empty = document.querySelector('[data-module-empty]');
  const filter = () => {
    const words = input.value.trim().toLowerCase().split(/\s+/).filter(Boolean);
    let visible = 0;
    for (const card of cards) {
      card.hidden = !words.every(word => card.dataset.search.includes(word));
      if (!card.hidden) visible++;
    }
    count.textContent = visible + (visible === 1 ? ' module shown.' : ' modules shown.');
    empty.hidden = visible !== 0;
  };
  tools.hidden = false;
  input.addEventListener('input', filter);
  filter();
}

// Relevance: title matches count most, then how often each word appears, then the
// whole phrase. Ties fall back to the title so results stay stable.
const occurrences = (text, word) => {
  let count = 0;
  for (let at = text.indexOf(word); at !== -1 && count < 25; at = text.indexOf(word, at + word.length)) count++;
  return count;
};
export const relevance = (entry, words, phrase) => {
  const title = entry.title.toLowerCase();
  const text = (entry.title + ' ' + entry.text).toLowerCase();
  if (!words.every(word => text.includes(word))) return 0;
  let score = 0;
  for (const word of words) score += (title.includes(word) ? 20 : 0) + occurrences(text, word) + (entry.summary.toLowerCase().includes(word) ? 3 : 0);
  if (words.length > 1) score += (title.includes(phrase) ? 30 : 0) + (text.includes(phrase) ? 10 : 0);
  return score;
};

// A short excerpt around the first match, with matches marked; built from text nodes, never HTML.
const snippet = (entry, words) => {
  const text = entry.text;
  const lower = text.toLowerCase();
  const first = Math.min(...words.map(word => lower.indexOf(word)).filter(at => at >= 0));
  const paragraph = document.createElement('p');
  if (!Number.isFinite(first)) { paragraph.textContent = entry.summary; return paragraph; }
  // Start at a word boundary so the excerpt never begins mid-word.
  let start = Math.max(0, first - 80);
  if (start > 0) start = Math.min(first, text.indexOf(' ', start) + 1 || start);
  const excerpt = (start ? '…' : '') + text.slice(start, first + 170) + (first + 170 < text.length ? '…' : '');
  const pattern = new RegExp('(' + words.map(word => word.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')', 'gi');
  for (const part of excerpt.split(pattern)) {
    if (!part) continue;
    if (words.includes(part.toLowerCase())) { const mark = document.createElement('mark'); mark.textContent = part; paragraph.append(mark); }
    else paragraph.append(document.createTextNode(part));
  }
  return paragraph;
};

const searchForm = document.querySelector('[data-site-search]');
if (searchForm) {
  const fallback = document.querySelector('[data-search-fallback]');
  const input = searchForm.querySelector('input');
  const status = document.querySelector('#search-status');
  const results = document.querySelector('#search-results');
  const indexURL = new URL(document.body.dataset.searchIndex, document.baseURI);
  // This is a generated static file hosted with the course, not a search service.
  fetch(indexURL).then(response => {
    if (!response.ok) throw new Error('Search index unavailable.');
    return response.json();
  }).then(entries => {
    searchForm.hidden = false;
    fallback.hidden = true;
    let timer;
    const search = () => {
      const query = input.value.trim().toLowerCase();
      results.replaceChildren();
      if (!query) { status.textContent = 'Enter a topic to search the reading pages.'; return; }
      const words = [...new Set(query.split(/\s+/).filter(Boolean))];
      const matches = entries.map(entry => ({ entry, score: relevance(entry, words, query) }))
        .filter(item => item.score > 0).sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title));
      for (const { entry } of matches.slice(0, 30)) {
        const item = document.createElement('li');
        const heading = document.createElement('h2');
        const anchor = document.createElement('a');
        anchor.href = new URL(entry.url, indexURL).href;
        anchor.textContent = entry.title;
        heading.append(anchor);
        item.append(heading, snippet(entry, words));
        results.append(item);
      }
      status.textContent = matches.length ? matches.length + ' matching pages, most relevant first.' + (matches.length > 30 ? ' Showing the first 30; use a more specific topic to narrow the results.' : '') : 'No matching pages. Try a broader topic or browse the module directory.';
    };
    input.value = new URL(location.href).searchParams.get('q') || '';
    searchForm.addEventListener('submit', event => {
      event.preventDefault();
      clearTimeout(timer);
      const url = new URL(location.href);
      if (input.value.trim()) url.searchParams.set('q', input.value.trim());
      else url.searchParams.delete('q');
      history.replaceState(null, '', url);
      search();
    });
    input.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(search, 200); });
    search();
  }).catch(() => {
    fallback.textContent = 'Search is unavailable in this view. Use the module directory and course outline to find a topic.';
    fallback.hidden = false;
  });
}
