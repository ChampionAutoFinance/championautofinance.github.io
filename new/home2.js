(() => {
  const menuToggle = document.getElementById('menuToggle');
  const nav = document.getElementById('siteNav');
  const progressBar = document.getElementById('progressBar');
  const yearLabel = document.getElementById('year');
  const leadForm = document.getElementById('leadForm');
  const formNote = document.getElementById('formNote');
  const heroTitle = document.getElementById('heroTitle');
  const storyCards = Array.from(document.querySelectorAll('.story'));
  const counters = Array.from(document.querySelectorAll('[data-count]'));
  const revealItems = Array.from(document.querySelectorAll('.reveal'));

  const heroPhrases = [
    'Confidence in every Mile',
    'Clear underwriting direction',
    'Built for dealer velocity',
    'Execution without surprises'
  ];

  if (menuToggle && nav) {
    menuToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });

    nav.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', () => {
        nav.classList.remove('is-open');
        menuToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  if (heroTitle) {
    let active = 0;
    setInterval(() => {
      active = (active + 1) % heroPhrases.length;
      heroTitle.style.opacity = '0';
      heroTitle.style.transform = 'translateY(12px)';
      setTimeout(() => {
        heroTitle.textContent = heroPhrases[active];
        heroTitle.style.opacity = '1';
        heroTitle.style.transform = 'translateY(0)';
      }, 200);
    }, 3200);
  }

  const reveal = () => {
    if (!('IntersectionObserver' in window)) {
      revealItems.forEach((el) => el.classList.add('is-visible'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries, observerRef) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const delay = Number(entry.target.style.getPropertyValue('--delay').replace('ms', '')) || 0;
          setTimeout(() => entry.target.classList.add('is-visible'), delay);
          observerRef.unobserve(entry.target);
        });
      },
      {
        threshold: 0.16
      }
    );

    revealItems.forEach((item) => observer.observe(item));
  };

  const animateCounters = () => {
    if (!counters.length) return;
    if (!('IntersectionObserver' in window)) {
      counters.forEach((counter) => {
        counter.textContent = counter.dataset.count;
      });
      return;
    }

    const countObserver = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const counter = entry.target;
          const target = Number(counter.dataset.count || '0');
          const duration = 1200;
          const start = performance.now();
          const from = 0;

          const tick = (time) => {
            const progress = Math.min((time - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            counter.textContent = Math.round(from + (target - from) * eased).toLocaleString();
            if (progress < 1) {
              requestAnimationFrame(tick);
            }
          };

          requestAnimationFrame(tick);
          obs.unobserve(counter);
        });
      },
      { threshold: 0.8 }
    );

    counters.forEach((counter) => countObserver.observe(counter));
  };

  const rotateStories = () => {
    if (!storyCards.length) return;
    let index = 0;
    storyCards[0].classList.add('is-active');

    setInterval(() => {
      const current = storyCards[index];
      current.classList.remove('is-active');
      index = (index + 1) % storyCards.length;
      const next = storyCards[index];
      next.classList.add('is-active');
    }, 4500);
  };

  const scrollBar = () => {
    const doc = document.documentElement;
    const max = doc.scrollHeight - doc.clientHeight;
    const value = max > 0 ? (window.scrollY / max) * 100 : 0;
    if (progressBar) progressBar.style.width = `${Math.min(value, 100)}%`;
  };

  const year = () => {
    if (yearLabel) yearLabel.textContent = new Date().getFullYear().toString();
  };

  if (leadForm) {
    leadForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const formData = Object.fromEntries(new FormData(leadForm));
      const email = String(formData.email || '').trim();
      const name = String(formData.name || '').trim();
      const message = String(formData.message || '').trim();

      if (!name || !message || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        if (formNote) formNote.textContent = 'Please fill in all fields with a valid email.';
        return;
      }

      if (formNote) formNote.textContent = `${name.split(' ')[0]}, your inquiry has been queued.`;
      leadForm.reset();
    });
  }

  let mouseX = 0;
  let mouseY = 0;
  document.addEventListener('pointermove', (event) => {
    mouseX = event.clientX / window.innerWidth;
    mouseY = event.clientY / window.innerHeight;

    const orbs = document.querySelectorAll('.bg-orb');
    orbs.forEach((orb, index) => {
      const x = (index === 0 ? -1 : 1) * (mouseX - 0.5) * 12;
      const y = (index === 0 ? -1 : 1) * (mouseY - 0.5) * 16;
      orb.style.transform = `translate(${x}px, ${y}px)`;
    });
  });

  year();
  reveal();
  animateCounters();
  rotateStories();
  scrollBar();
  window.addEventListener('scroll', scrollBar, { passive: true });
})();
