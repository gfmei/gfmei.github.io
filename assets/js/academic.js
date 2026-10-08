(() => {
  const toggle = document.querySelector('.navbar-toggler');
  const navigation = document.getElementById('navbarNav');
  const navbar = document.getElementById('navbar');
  const progress = document.getElementById('progress');
  toggle.addEventListener('click', () => {
    const expanded = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(expanded));
    toggle.classList.toggle('collapsed', !expanded);
    navigation.classList.toggle('show', expanded);
  });
  let scheduled = false;
  function updateProgress() {
    progress.max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
    progress.value = window.scrollY;
    progress.style.top = `${navbar.offsetHeight}px`;
    scheduled = false;
  }
  function scheduleProgress() {
    if (!scheduled) {
      scheduled = true;
      requestAnimationFrame(updateProgress);
    }
  }
  window.addEventListener('scroll', scheduleProgress, { passive: true });
  window.addEventListener('resize', scheduleProgress);
  window.addEventListener('load', scheduleProgress);
  updateProgress();
})();
