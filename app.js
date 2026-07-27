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

// Re-anchor a hash landing after fonts settle (one-page layout: sections shift as the
// display font swaps in, so the browser's initial hash jump can land short)
if (location.hash) {
  const target = document.querySelector(location.hash);
  if (target) window.addEventListener('load', () => {
    (document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve())
      .then(() => target.scrollIntoView());
  });
}

// Scroll reveals
const io = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
}, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Instagram embeds: pull in IG's script only when the section nears the viewport, so the
// hero's LCP never pays for it. Never loads at all when IG_POSTS is empty (no section).
const igGrid = document.getElementById('ig-grid');
if (igGrid) {
  const igIO = new IntersectionObserver((entries) => {
    if (!entries.some(e => e.isIntersecting)) return;
    igIO.disconnect();
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.instagram.com/embed.js';
    document.body.appendChild(s);
  }, { rootMargin: '600px 0px' });
  igIO.observe(igGrid);
}

// Nav scrollspy (one-page layout): highlight the section currently under the header.
// build.py renders #top active server-side; this keeps it in step as you scroll.
// No CSS needed, .nav-links a.active is already styled.
const spy = [...document.querySelectorAll('.nav-links a[href^="#"]')]
  .map(a => ({ a, sec: document.querySelector(a.getAttribute('href')) }))
  .filter(x => x.sec);
if (spy.length > 1) {
  const NAV_H = 100;              // sections use scroll-margin-top:92px
  let current = null;
  const sync = () => {
    const y = scrollY + NAV_H + 1;
    // last section whose top has passed under the header; sections vary a lot in
    // height, so this is steadier than raw intersection ratios
    let active = spy[0];
    for (const x of spy) if (x.sec.getBoundingClientRect().top + scrollY <= y) active = x;
    // the final section is often shorter than the viewport and can never reach the
    // header, so it would otherwise never light up
    if (innerHeight + scrollY >= document.body.scrollHeight - 2) active = spy[spy.length - 1];
    if (active === current) return;
    current = active;
    spy.forEach(x => {
      x.a.classList.toggle('active', x === active);
      if (x === active) x.a.setAttribute('aria-current', 'true');
      else x.a.removeAttribute('aria-current');
    });
  };
  // Called straight from the scroll event, no rAF wrapper: the browser already fires
  // scroll at most once a frame, and rAF is suspended in a hidden tab (which also made
  // this impossible to test).
  addEventListener('scroll', sync, { passive: true });
  addEventListener('resize', sync);
  sync();
}

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
