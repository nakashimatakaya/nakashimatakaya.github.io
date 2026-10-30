'use strict';
(() => {
  const root = document.documentElement;
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#site-nav');
  const motionButton = document.querySelector('.motion-toggle');
  const progress = document.querySelector('.scroll-progress');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const revealElements = [...document.querySelectorAll('[data-reveal]')];
  const isEnglish = root.lang === 'en';
  let observer;
  let paused = false;
  try { paused = localStorage.getItem('portfolio-motion') === 'paused'; } catch (_) {}

  function closeMenu() {
    menuButton.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
  }
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  navigation.addEventListener('click', event => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menuButton.focus();
    }
  });
  window.matchMedia('(min-width: 1181px)').addEventListener('change', event => {
    if (event.matches) closeMenu();
  });
  document.querySelector('.site-header').addEventListener('focusout', event => {
    if (!event.currentTarget.contains(event.relatedTarget)) closeMenu();
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  root.classList.add('js-enabled');
  document.querySelector('.hero-photo img').addEventListener('animationend', event => {
    if (event.animationName === 'portrait-unveil') root.classList.remove('hero-motion');
  });

  function revealAnchor() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const target = document.getElementById(id);
    if (!target) return;
    let ancestor = target.closest('details');
    let opened = false;
    while (ancestor) {
      if (!ancestor.open) { ancestor.open = true; opened = true; }
      ancestor = ancestor.parentElement.closest('details');
    }
    target.closest('[data-reveal]')?.classList.add('is-in');
    if (opened) requestAnimationFrame(() => target.scrollIntoView({ behavior: 'instant' }));
  }
  window.addEventListener('hashchange', revealAnchor);
  revealAnchor();

  function configureMotion() {
    const enabled = !paused && !reducedMotion.matches;
    root.dataset.motion = enabled ? 'on' : 'off';
    motionButton.hidden = false;
    motionButton.setAttribute('aria-pressed', String(enabled));
    motionButton.setAttribute('aria-disabled', String(reducedMotion.matches));
    motionButton.title = reducedMotion.matches
      ? (isEnglish ? 'Motion is off in your device settings' : '端末の設定で動きを停止しています')
      : enabled ? (isEnglish ? 'Pause motion' : '動きを止める')
      : (isEnglish ? 'Enable motion' : '動きを再開する');
    motionButton.querySelector('[aria-hidden]').textContent = enabled ? 'Ⅱ' : '▷';
    if (!enabled) root.classList.remove('hero-motion');
    observer?.disconnect();
    if (enabled && 'IntersectionObserver' in window) {
      observer = new IntersectionObserver(entries => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            observer.unobserve(entry.target);
          }
        }
      }, { threshold: 0.08, rootMargin: '0px 0px -32px 0px' });
      revealElements.forEach(element => observer.observe(element));
      root.classList.add('motion-ready');
    } else {
      revealElements.forEach(element => element.classList.add('is-in'));
      root.classList.remove('motion-ready');
    }
  }
  motionButton.addEventListener('click', () => {
    if (reducedMotion.matches) return;
    paused = !paused;
    try { localStorage.setItem('portfolio-motion', paused ? 'paused' : 'on'); } catch (_) {}
    configureMotion();
  });
  reducedMotion.addEventListener('change', configureMotion);
  // Focused content is always visible, including keyboard navigation into a section.
  document.addEventListener('focusin', event => event.target.closest('[data-reveal]')?.classList.add('is-in'));
  configureMotion();

  let framePending = false;
  function updateProgress() {
    const range = root.scrollHeight - window.innerHeight;
    const fraction = range > 0 ? Math.max(0, Math.min(1, window.scrollY / range)) : 0;
    progress.style.transform = `scaleX(${fraction})`;
    framePending = false;
  }
  function queueProgress() {
    if (!framePending) { framePending = true; requestAnimationFrame(updateProgress); }
  }
  window.addEventListener('scroll', queueProgress, { passive: true });
  window.addEventListener('resize', queueProgress);
  document.querySelectorAll('details').forEach(element => element.addEventListener('toggle', queueProgress));
  updateProgress();

  let closedBeforePrint = [];
  window.addEventListener('beforeprint', () => {
    closedBeforePrint = [...document.querySelectorAll('details:not([open])')];
    closedBeforePrint.forEach(element => { element.open = true; });
  });
  window.addEventListener('afterprint', () => {
    closedBeforePrint.forEach(element => { element.open = false; });
    closedBeforePrint = [];
    queueProgress();
  });
})();
