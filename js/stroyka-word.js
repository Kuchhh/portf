/* «Стройка»: надпись СТРОЙКА летает по квадратному блоку как твёрдое тело.
   Гравитация плавно меняет направление, надпись отскакивает от стенок и вращается.
   Настройки перенесены из генератора Cascade Type (mockups/cascade-type). */
(function () {
  'use strict';

  const box = document.getElementById('stroykaWord');
  if (!box) return;
  const canvas = box.querySelector('canvas');
  const ctx = canvas.getContext('2d');

  const S = {
    text: 'СТРОЙКА',
    font: '700 101px "Poster Bodoni", serif',
    size: 101,
    stretchY: 2.3,
    color: '#F4DE4D',
    background: '#191919',
    angle: -320 * Math.PI / 180,
    restitution: 1,
    friction: 0.1,
    airFriction: 0.01,
    gravity: { minX: 1, maxX: -1, minY: 1, maxY: -1, speed: 1.5, randomness: 0.2 },
  };
  const WORLD = 1080;          // физика считается в кадре 1080×1080, на экран — масштаб
  const STEP = 1000 / 60;
  const G_PER_STEP = 0.256;    // ускорение гравитации за шаг 16 мс (как в matter.js)
  const REST_SPEED = 2;        // медленнее этого — не отскакивает, а ложится

  let body = null;
  let simStep = 0;

  function gravityAt(t) {
    const g = S.gravity, a = t * g.speed;
    const chaosX = (Math.sin(a) + Math.sin(a * 1.34 + 1.5) + Math.sin(a * 0.87 + 2.1)) / 3;
    const chaosY = (Math.cos(a) + Math.cos(a * 1.34 + 1.5) + Math.cos(a * 0.87 + 2.1)) / 3;
    const wx = Math.sin(a) + (chaosX - Math.sin(a)) * g.randomness;
    const wy = Math.cos(a) + (chaosY - Math.cos(a)) * g.randomness;
    return {
      x: g.minX + (g.maxX - g.minX) * (wx * 0.5 + 0.5),
      y: g.minY + (g.maxY - g.minY) * (wy * 0.5 + 0.5),
    };
  }

  function makeBody() {
    ctx.font = S.font;
    const hw = ctx.measureText(S.text).width / 2;
    const hh = (S.size * 0.75 * S.stretchY) / 2;
    return {
      x: WORLD / 2, y: WORLD / 2, vx: 0, vy: 0,
      a: S.angle, va: 0, hw, hh,
      invI: 12 / (4 * hw * hw + 4 * hh * hh), // масса 1
    };
  }

  // соударение углов прямоугольника со стенками: импульс по нормали + трение
  function collide(b) {
    const c = Math.cos(b.a), s = Math.sin(b.a);
    for (const [sx, sy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) {
      const rx = sx * b.hw * c - sy * b.hh * s;
      const ry = sx * b.hw * s + sy * b.hh * c;
      const px = b.x + rx, py = b.y + ry;
      const walls = [[px, 1, 0], [WORLD - px, -1, 0], [py, 0, 1], [WORLD - py, 0, -1]];
      for (const [gap, nx, ny] of walls) {
        if (gap >= 0) continue;
        const vpx = b.vx - b.va * ry, vpy = b.vy + b.va * rx;
        const vn = vpx * nx + vpy * ny;
        if (vn < 0) {
          const e = -vn < REST_SPEED ? 0 : S.restitution;
          const rn = rx * ny - ry * nx;
          const j = -(1 + e) * vn / (1 + rn * rn * b.invI);
          b.vx += j * nx; b.vy += j * ny; b.va += rn * j * b.invI;
          const tx = -ny, ty = nx;
          const vt = (b.vx - b.va * ry) * tx + (b.vy + b.va * rx) * ty;
          const rt = rx * ty - ry * tx;
          let jt = -vt / (1 + rt * rt * b.invI);
          jt = Math.max(-S.friction * j, Math.min(S.friction * j, jt));
          b.vx += jt * tx; b.vy += jt * ty; b.va += rt * jt * b.invI;
        }
        b.x += -gap * nx; b.y += -gap * ny; // выталкиваем из стенки
      }
    }
  }

  function step() {
    const g = gravityAt(simStep / 60);
    const b = body;
    b.vx = (b.vx + g.x * G_PER_STEP) * (1 - S.airFriction);
    b.vy = (b.vy + g.y * G_PER_STEP) * (1 - S.airFriction);
    b.va *= 1 - S.airFriction;
    b.x += b.vx; b.y += b.vy; b.a += b.va;
    for (let i = 0; i < 3; i++) collide(b);
    simStep++;
  }

  function resize() {
    const k = Math.min(window.devicePixelRatio || 1, 2);
    const w = Math.max(1, Math.round(box.clientWidth * k));
    const h = Math.max(1, Math.round(box.clientHeight * k));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; draw(); }
  }

  function draw() {
    const w = canvas.width, h = canvas.height;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.fillStyle = S.background;
    ctx.fillRect(0, 0, w, h);
    if (!body) return;
    const k = w / WORLD;
    ctx.setTransform(k, 0, 0, k, 0, 0);
    ctx.translate(body.x, body.y);
    ctx.rotate(body.a);
    ctx.scale(1, S.stretchY);
    ctx.font = S.font;
    ctx.fillStyle = S.color;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(S.text, 0, 0);
  }

  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  let visible = false, raf = 0, last = 0, acc = 0;
  function frame(now) {
    raf = 0;
    acc += last ? Math.min(100, now - last) : 0;
    last = now;
    while (acc >= STEP) { step(); acc -= STEP; }
    draw();
    if (visible && !document.hidden) raf = requestAnimationFrame(frame);
  }
  function wake() {
    if (!raf && visible && !still && !document.hidden && body) { last = 0; raf = requestAnimationFrame(frame); }
  }

  new ResizeObserver(resize).observe(box);
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; wake(); }).observe(box);
  document.addEventListener('visibilitychange', wake);

  // шрифт встроен в js/stroyka-font.js: так он грузится и при открытии сайта с диска
  const fontReady = window.POSTER_BODONI_DATA
    ? new FontFace('Poster Bodoni', `url(${window.POSTER_BODONI_DATA})`).load().then((f) => document.fonts.add(f))
    : document.fonts.load(S.font);
  fontReady.catch(() => {}).then(() => {
    body = makeBody();
    resize();
    draw();
    wake();
  });
})();
