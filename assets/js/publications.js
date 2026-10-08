(() => {
  const search = document.getElementById('paper-search');
  const year = document.getElementById('paper-year');
  const type = document.getElementById('paper-type');
  const cards = [...document.querySelectorAll('.paper-card')];
  const sections = [...document.querySelectorAll('.publication-year')];
  const count = document.getElementById('publication-count');
  const empty = document.getElementById('publication-empty');
  const searchableText = new Map(cards.map(card => [card, card.textContent.toLocaleLowerCase()]));
  document.querySelector('.publication-controls').hidden = false;
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    cards.forEach(card => {
      card.hidden = !(searchableText.get(card).includes(query) && (year.value === 'all' || card.dataset.year === year.value) && (type.value === 'all' || card.dataset.type === type.value));
      if (!card.hidden) visible++;
    });
    sections.forEach(section => {
      const matches = [...section.querySelectorAll('.paper-card')].filter(card => !card.hidden).length;
      section.hidden = matches === 0;
      section.querySelector('.year-heading span').textContent = `${matches} ${matches === 1 ? 'work' : 'works'}`;
    });
    count.textContent = `${visible} ${visible === 1 ? 'research work' : 'research works'}`;
    empty.hidden = visible !== 0;
  }
  document.querySelectorAll('.publication-year-nav a').forEach(link => {
    link.addEventListener('click', event => {
      event.preventDefault();
      search.value = '';
      year.value = 'all';
      type.value = 'all';
      filter();
      const heading = document.querySelector(link.getAttribute('href'));
      heading.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' });
      history.replaceState(null, '', link.getAttribute('href'));
    });
  });
  search.addEventListener('input', filter);
  year.addEventListener('change', filter);
  type.addEventListener('change', filter);
  // The page remains browsable without the Bootstrap JavaScript bundle.
  const toggle = document.querySelector('.navbar-toggler');
  const navigation = document.getElementById('navbarNav');
  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(expanded));
    toggle.classList.toggle('collapsed', !expanded);
    navigation.classList.toggle('show', expanded);
  });
})();
