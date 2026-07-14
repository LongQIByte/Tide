(function () {
  const deck = document.getElementById('deck');
  const launcher = document.getElementById('launcher');
  if (!deck || !launcher) return;
  const slides = deck.querySelectorAll('.slide');
  const dots = deck.querySelectorAll('.dot');
  const cur = deck.querySelector('.count b');
  const prev = deck.querySelector('.prev');
  const next = deck.querySelector('.next');
  let i = 0;
  function go(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((s, k) => s.classList.toggle('active', k === i));
    dots.forEach((d, k) => d.classList.toggle('active', k === i));
    cur.textContent = i + 1;
    prev.disabled = i === 0;
    next.disabled = i === slides.length - 1;
    slides[i].querySelector('.note').scrollTop = 0;
  }
  prev.onclick = () => go(i - 1);
  next.onclick = () => go(i + 1);
  dots.forEach((d, k) => d.onclick = () => go(k));
  function open() {
    deck.classList.add('open');
    document.body.style.overflow = 'hidden';
    if (deck.requestFullscreen) deck.requestFullscreen().catch(() => {});
    go(i);
  }
  function close() {
    deck.classList.remove('open');
    document.body.style.overflow = '';
    if (document.fullscreenElement) document.exitFullscreen();
  }
  launcher.onclick = open;
  deck.querySelector('.close').onclick = close;
  document.addEventListener('fullscreenchange', () => {
    if (!document.fullscreenElement && deck.classList.contains('open')) {
      deck.classList.remove('open');
      document.body.style.overflow = '';
    }
  });
  document.addEventListener('keydown', (e) => {
    if (!deck.classList.contains('open')) return;
    if (e.key === 'ArrowRight' || e.key === ' ') {
      e.preventDefault();
      go(i + 1);
    } else if (e.key === 'ArrowLeft') {
      e.preventDefault();
      go(i - 1);
    } else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      const note = slides[i].querySelector('.note');
      note.scrollBy({ top: e.key === 'ArrowDown' ? 120 : -120, behavior: 'smooth' });
    } else if (e.key === 'Escape') {
      close();
    }
  });
})();
