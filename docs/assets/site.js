// Optional enhancements. Reading, module links, and native disclosures still
// work without JavaScript. Search stays in this browser; no query is sent away.
const outline = document.querySelector('[data-course-outline]');
if (outline && window.matchMedia('(min-width: 64rem)').matches) outline.open = true;

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
      const words = query.split(/\s+/).filter(Boolean);
      const matches = entries.map(entry => {
        const title = entry.title.toLowerCase();
        const text = (entry.title + ' ' + entry.text).toLowerCase();
        return { entry, score: words.every(word => text.includes(word)) ? words.reduce((total, word) => total + (title.includes(word) ? 3 : 1), 0) : 0 };
      }).filter(item => item.score > 0).sort((a, b) => b.score - a.score || a.entry.title.localeCompare(b.entry.title));
      for (const { entry } of matches.slice(0, 30)) {
        const item = document.createElement('li');
        const heading = document.createElement('h2');
        const anchor = document.createElement('a');
        anchor.href = new URL(entry.url, indexURL).href;
        anchor.textContent = entry.title;
        heading.append(anchor);
        const summary = document.createElement('p');
        summary.textContent = entry.summary;
        item.append(heading, summary);
        results.append(item);
      }
      status.textContent = matches.length ? matches.length + ' matching pages.' + (matches.length > 30 ? ' Showing the first 30; use a more specific topic to narrow the results.' : '') : 'No matching pages. Try a broader topic or browse the module directory.';
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
