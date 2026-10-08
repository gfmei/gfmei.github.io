(() => {
  const banner = document.querySelector('.collaboration-banner');
  if (!banner) return;
  const button = banner.querySelector('.collaboration-pause');
  button.hidden = false;
  button.addEventListener('click', () => {
    const paused = banner.classList.toggle('is-paused');
    button.setAttribute('aria-pressed', String(paused));
    button.setAttribute('aria-label', paused ? 'Resume scrolling invitation' : 'Pause scrolling invitation');
    button.querySelector('i').className = paused ? 'fas fa-play' : 'fas fa-pause';
  });
})();
