(() => {
  const navToggle = document.getElementById('menuToggle');
  const primaryNav = document.getElementById('primaryMenu');
  const readProgress = document.getElementById('readProgress');
  const leadForm = document.getElementById('leadForm');
  const formNote = document.getElementById('formNote');
  const heroHeadline = document.getElementById('heroHeadline');
  const backToTop = document.getElementById('backToTop');
  const yearNode = document.getElementById('year');
  const revealTargets = Array.from(document.querySelectorAll('.reveal'));
  const countNodes = Array.from(document.querySelectorAll('[data-count]'));

  const headlineSequence = [
    'Fast approvals. Compliant execution. Predictable outcomes.',
    'High-signal underwriting guidance at every turn.',
    'Dealer workflows engineered for real speed.',
    'Institutional-grade process, startup velocity.'
  ];

  const safeNum = (value) => Number(String(value || '').replace(/[^0-9.-]/g, '') || 0);

  const toggleNav = () => {
    if (!navToggle || !primaryNav) return;
    const isOpen = primaryNav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  };

  if (navToggle) {
    navToggle.addEventListener('click', toggleNav);
    primaryNav.querySelectorAll('a').forEach((anchor) => {
      anchor.addEventListener('click', () => {
        primaryNav.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  const cycleHeadline = () => {
    if (!heroHeadline) return;
    let index = 0;
    setInterval(() => {
      index = (index + 1) % headlineSequence.length;
      heroHeadline.style.opacity = '0';
      heroHeadline.style.transform = 'translateY(10px)';
      setTimeout(() => {
        heroHeadline.textContent = headlineSequence[index];
        heroHeadline.style.opacity = '1';
        heroHeadline.style.transform = 'translateY(0)';
      }, 220);
    }, 3600);
  };

  const revealSections = () => {
    if (!('IntersectionObserver' in window)) {
      revealTargets.forEach((el) => el.classList.add('is-visible'));
      return;
    }

    const observer = new IntersectionObserver(
      (entries, io) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const delay = safeNum(entry.target.style.getPropertyValue('--delay'));
          setTimeout(() => entry.target.classList.add('is-visible'), delay);
          io.unobserve(entry.target);
        });
      },
      {
        threshold: 0.16
      }
    );

    revealTargets.forEach((target) => observer.observe(target));
  };

  const animateCounters = () => {
    if (!countNodes.length) return;
    if (!('IntersectionObserver' in window)) {
      countNodes.forEach((node) => {
        node.textContent = safeNum(node.dataset.count).toLocaleString();
      });
      return;
    }

    const counterObserver = new IntersectionObserver(
      (entries, io) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const node = entry.target;
          const targetValue = safeNum(node.dataset.count);
          const start = performance.now();
          const duration = 1300;
          const startValue = 0;

          const update = (time) => {
            const progress = Math.min((time - start) / duration, 1);
            const eased = 1 - Math.pow(1 - progress, 3);
            node.textContent = Math.round(startValue + (targetValue - startValue) * eased).toLocaleString();
            if (progress < 1) requestAnimationFrame(update);
          };

          requestAnimationFrame(update);
          io.unobserve(node);
        });
      },
      { threshold: 0.7 }
    );

    countNodes.forEach((node) => counterObserver.observe(node));
  };

  const bindProgressBar = () => {
    const update = () => {
      const doc = document.documentElement;
      const max = doc.scrollHeight - doc.clientHeight;
      const value = max > 0 ? (window.scrollY / max) * 100 : 0;
      if (readProgress) readProgress.style.width = `${Math.min(value, 100)}%`;
      if (backToTop) {
        if (window.scrollY > 420) {
          backToTop.classList.add('is-visible');
        } else {
          backToTop.classList.remove('is-visible');
        }
      }
    };
    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
  };

  const bindBackToTop = () => {
    if (!backToTop) return;
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  };

  const bindForm = () => {
    if (!leadForm) return;
    leadForm.addEventListener('submit', (event) => {
      event.preventDefault();
      const formData = Object.fromEntries(new FormData(leadForm));
      const name = String(formData.name || '').trim();
      const email = String(formData.email || '').trim();
      const message = String(formData.message || '').trim();
      const isEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

      if (!name || !message || !isEmail) {
        if (formNote) {
          formNote.textContent = 'Please fill all fields with a valid email.';
        }
        return;
      }

      if (formNote) {
        formNote.textContent = `${name.split(' ')[0]}, your request is in queue.`;
      }
      leadForm.reset();
    });
  };

  const addAmbientMotion = () => {
    const ambientOne = document.querySelector('.ambient--one');
    const ambientTwo = document.querySelector('.ambient--two');
    if (!ambientOne || !ambientTwo || !('ontouchstart' in window)) return;

    document.addEventListener('pointermove', (event) => {
      const x = (event.clientX / window.innerWidth - 0.5) * 16;
      const y = (event.clientY / window.innerHeight - 0.5) * 10;
      ambientOne.style.transform = `translate(${x * -1}px, ${y * -0.8}px)`;
      ambientTwo.style.transform = `translate(${x * 0.9}px, ${y * -0.5}px)`;
    });
  };

  const year = () => {
    if (yearNode) yearNode.textContent = new Date().getFullYear();
  };

  year();
  revealSections();
  animateCounters();
  cycleHeadline();
  bindProgressBar();
  bindBackToTop();
  bindForm();
  addAmbientMotion();
})();
