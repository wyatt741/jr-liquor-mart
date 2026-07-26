// B Printing and Wraps - mobile menu, scroll reveals, gallery filter, lightbox
// Mobile menu
const burger = document.querySelector('.burger');
if (burger) {
  const toggle = (open) => { document.body.classList.toggle('menu-open', open); burger.setAttribute('aria-expanded', open); };
  burger.addEventListener('click', () => toggle(!document.body.classList.contains('menu-open')));
  document.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', () => toggle(false)));
  document.addEventListener('keydown', e => { if (e.key === 'Escape') toggle(false); });
}

// Theme toggle (dark default via FOUC script in <head>; choice persists)
document.querySelectorAll('.theme-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const dark = document.documentElement.getAttribute('data-theme') === 'dark';
    const next = dark ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('theme', next); } catch (e) {}
  });
});

// Scroll reveals
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Gallery filter
const filters = document.querySelectorAll('.gfilter');
if (filters.length) {
  const tiles = document.querySelectorAll('#gal .tile');
  filters.forEach(btn => btn.addEventListener('click', () => {
    filters.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.getAttribute('data-cat');
    tiles.forEach(t => t.classList.toggle('hide', cat !== 'all' && t.getAttribute('data-cat') !== cat));
  }));
}

// Lightbox (gallery)
const lb = document.getElementById('lightbox');
if (lb) {
  const lbImg = lb.querySelector('img');
  const open = (src, alt) => { lbImg.src = src; lbImg.alt = alt || ''; lb.classList.add('on'); lb.setAttribute('aria-hidden', 'false'); };
  const close = () => { lb.classList.remove('on'); lb.setAttribute('aria-hidden', 'true'); lbImg.src = ''; };
  document.querySelectorAll('#gal .tile[data-full]').forEach(t => {
    const go = () => open(t.getAttribute('data-full'), t.querySelector('img')?.alt);
    t.addEventListener('click', go);
    t.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(); } });
  });
  lb.addEventListener('click', e => { if (e.target !== lbImg) close(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
}
