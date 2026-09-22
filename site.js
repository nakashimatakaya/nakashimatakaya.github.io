'use strict';
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#site-nav');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('is-open');
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
navigation.addEventListener('click', (event) => {
  if (event.target.closest('a')) closeMenu();
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
window.matchMedia('(min-width: 851px)').addEventListener('change', (event) => {
  if (event.matches) closeMenu();
});
// Open a collapsed section when a direct link targets content inside it.
function revealAnchor() {
  const target = document.getElementById(location.hash.slice(1));
  if (!target) return;
  let section = target.closest('details');
  while (section) {
    section.open = true;
    section = section.parentElement.closest('details');
  }
}
window.addEventListener('hashchange', revealAnchor);
revealAnchor();

document.documentElement.classList.add('js-enabled');
