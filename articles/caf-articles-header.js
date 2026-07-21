(() => {
  const header = document.getElementById('cafArticleNav');
  const toggle = document.getElementById('cafArticleNavToggle');
  const menu = document.getElementById('cafArticleMenu');

  if (!header || !toggle || !menu) return;

  const setOpen = (open) => {
    header.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  };

  toggle.addEventListener('click', () => {
    setOpen(!header.classList.contains('is-open'));
  });

  menu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setOpen(false));
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') setOpen(false);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 960) setOpen(false);
  });
})();
