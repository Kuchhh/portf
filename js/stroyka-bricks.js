/* «Стройка»: стеклянные кирпичи падают на постер (WebGL). Перенесено из stroyka-embed.zip;
   фон берётся из js/stroyka-bricks-bg.js, чтобы текстура работала и при открытии сайта с диска. */
(function () {
  'use strict';
  // Settings fixed from the designer's tool export.
  const S = { size: 0.7, count: 3, spread: 1, speed: 0.15, ior: 1.4, bgZ: 0.75, disp: 0.041, rainbow: 1.2,
    tint: [0xD9 / 255, 0xD9 / 255, 0xD9 / 255], reflect: 1.55, edge: 0.084, bg: window.STROYKA_BRICKS_BG || 'assets/img/stroyka/bricks-bg.webp' };
  const MM = 1 / 125;
  const HALF = [1.0, 44 * MM, 60 * MM];                         // полуторный 250×120×88
  const HOLES = { nx: 3, step: 74 * MM, half: [25 * MM, 23 * MM], r: 16 * MM }; // 3 отверстия
  const MAX = 3;

  const box = document.getElementById('stroykaBricks');
  if (!box) return;
  const canvas = box.querySelector('canvas');
  const gl = canvas.getContext('webgl2', { alpha: true, premultipliedAlpha: true, antialias: false });
  if (!gl) return; // the CSS background image stays as a still fallback

  const FRAG = `#version 300 es
precision highp float;
out vec4 outColor;
uniform vec2 uRes;
uniform vec3 uBPos[${MAX}];
uniform mat3 uBRot[${MAX}];
uniform float uBScale[${MAX}];
uniform sampler2D uBg;
uniform vec2 uBgScale;
uniform float uLodBase;
const vec3 HALF = vec3(${HALF.map(v => v.toFixed(5)).join(',')});
const float EDGE = ${S.edge.toFixed(4)};
const float HSTEP = ${HOLES.step.toFixed(5)};
const vec2 HHALF = vec2(${HOLES.half.map(v => v.toFixed(5)).join(',')});
const float HR = ${HOLES.r.toFixed(5)};
const float IOR = ${S.ior.toFixed(3)};
const float DISP = ${S.disp.toFixed(4)};
const float RAINBOW = ${S.rainbow.toFixed(3)};
const float REFLECT = ${S.reflect.toFixed(3)};
const float BGZ = ${S.bgZ.toFixed(3)};
const vec3 TINT = vec3(${S.tint.map(v => v.toFixed(4)).join(',')});
const float CAM_D = 7.0;
const float BOUND = ${(Math.hypot(...HALF) + 0.03).toFixed(4)};

float sdRoundBox(vec3 p, vec3 b, float r) { vec3 q = abs(p) - b + r; return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - r; }
float sdRoundRect(vec2 p, vec2 b, float r) { vec2 q = abs(p) - b + r; return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r; }
float brick(vec3 q) {
  float d = sdRoundBox(q, HALF, EDGE);
  if (d > 0.3) return d;
  float x = q.x - clamp(floor(q.x / HSTEP + 1.5), 0.0, 2.0) * HSTEP + HSTEP;
  return max(d, -sdRoundRect(vec2(x, q.z), HHALF, HR));
}
float map(vec3 p) {
  float d = 1e9;
  for (int i = 0; i < ${MAX}; i++) {
    float s = uBScale[i];
    float bs = length(p - uBPos[i]) - BOUND * s;
    if (bs > 0.04 * s) { d = min(d, bs); continue; }
    d = min(d, brick(uBRot[i] * (p - uBPos[i]) / s) * s);
  }
  return d;
}
vec3 calcNormal(vec3 p) {
  const vec2 k = vec2(1.0, -1.0); float e = 0.001;
  return normalize(k.xyy * map(p + k.xyy * e) + k.yyx * map(p + k.yyx * e) + k.yxy * map(p + k.yxy * e) + k.xxx * map(p + k.xxx * e));
}
float softbox(vec3 d, vec3 c, vec2 size) {
  c = normalize(c);
  vec3 x = normalize(cross(vec3(0.0, 1.0, 0.001), c)), y = cross(c, x);
  float z = dot(d, c);
  if (z <= 0.0) return 0.0;
  vec2 uv = abs(vec2(dot(d, x), dot(d, y)) / z) / size;
  return 1.0 - smoothstep(0.82, 1.0, max(uv.x, uv.y));
}
vec3 env(vec3 d) {
  vec3 c = mix(vec3(0.16, 0.17, 0.17), vec3(0.78, 0.79, 0.80), smoothstep(-0.7, 0.9, d.y));
  c += 1.9 * softbox(d, vec3(-0.55, 0.85, 0.6), vec2(0.55, 0.32));
  c += 1.4 * softbox(d, vec3(0.95, 0.15, 0.45), vec2(0.07, 0.75));
  c += vec3(0.85, 0.92, 1.0) * 0.9 * softbox(d, vec3(-0.9, 0.05, -0.4), vec2(0.06, 0.6));
  c += 0.6 * softbox(d, vec3(0.1, -0.2, 1.0), vec2(0.9, 0.08));
  return c;
}
vec3 bgAt(vec2 s) {
  vec2 uv = vec2(s.x / (uRes.x / uRes.y) * 0.5 + 0.5, s.y * 0.5 + 0.5);
  return textureLod(uBg, clamp((uv - 0.5) * uBgScale + 0.5, 0.0, 1.0), uLodBase).rgb;
}
vec3 backdrop(vec3 pos, vec3 d) {
  vec3 e = env(d) * 0.85;
  if (-d.z < 0.02) return e;
  vec3 hp = pos + d * ((-BGZ - pos.z) / d.z);
  return mix(e, bgAt(hp.xy * CAM_D / (CAM_D + BGZ)), smoothstep(0.02, 0.2, -d.z));
}
float marchOut(vec3 ro, vec3 rd) {
  float t = 0.007;
  for (int i = 0; i < 80; i++) { float d = map(ro + rd * t); if (d < 0.0004) return t; t += d * 0.8; if (t > 8.0) break; }
  return -1.0;
}
float marchIn(vec3 ro, vec3 rd) {
  float t = 0.003;
  for (int i = 0; i < 56; i++) { float d = -map(ro + rd * t); if (d < 0.0004) return t; t += max(d * 0.8, 0.001); if (t > 4.0) break; }
  return t;
}
vec3 shade(vec3 p, vec3 rd) {
  vec3 n = calcNormal(p);
  float cosi = clamp(dot(-rd, n), 0.0, 1.0);
  float f0 = pow((IOR - 1.0) / (IOR + 1.0), 2.0);
  float fr = f0 + (1.0 - f0) * pow(1.0 - cosi, 5.0);
  vec3 dir = refract(rd, n, 1.0 / IOR);
  vec3 pos = p, lastIn = dir, lastN = n;
  float path = 0.0, loss = 1.0;
  bool inside = true, exited = false;
  for (int k = 0; k < 6; k++) {
    if (inside) {
      float t = marchIn(pos, dir); pos += dir * t; path += t;
      vec3 ne = calcNormal(pos);
      vec3 o = refract(dir, -ne, IOR);
      if (dot(o, o) < 1e-5) { dir = reflect(dir, -ne); loss *= 0.93; }
      else { lastIn = dir; lastN = ne; dir = o; inside = false; exited = true; }
    } else {
      float t = marchOut(pos, dir);
      if (t < 0.0) break;
      pos += dir * t;
      vec3 n2 = calcNormal(pos);
      vec3 i2 = refract(dir, n2, 1.0 / IOR);
      if (dot(i2, i2) < 1e-5) dir = reflect(dir, n2); else { dir = i2; inside = true; }
    }
  }
  vec3 tr;
  vec3 dR = refract(lastIn, -lastN, max(1.0, IOR - DISP * 3.0)), dB = refract(lastIn, -lastN, IOR + DISP * 3.0);
  if (exited && !inside && dot(dR, dR) > 1e-5 && dot(dB, dB) > 1e-5) {
    dR = normalize(dir + clamp(dR - dir, -0.08, 0.08));
    dB = normalize(dir + clamp(dB - dir, -0.08, 0.08));
    tr = vec3(backdrop(pos, dR).r, backdrop(pos, dir).g, backdrop(pos, dB).b);
  } else tr = backdrop(pos, dir);
  tr *= pow(TINT, vec3(0.8 + path / 0.7 * 1.6)) * loss;
  vec3 rainbow = 0.5 + 0.5 * cos(6.28318 * (vec3(0.0, 0.33, 0.67) + dot(n, vec3(0.35, 0.8, 1.1)) * 0.9));
  vec3 col = tr * (1.0 - fr);
  col += env(reflect(rd, n)) * fr * REFLECT * 1.4;
  col += rainbow * pow(1.0 - cosi, 2.0) * RAINBOW * (0.3 + REFLECT * 0.7);
  return clamp(col, 0.0, 1.0);
}
void main() {
  vec2 sp = (2.0 * gl_FragCoord.xy - uRes) / uRes.y;
  vec3 ro = vec3(0.0, 0.0, CAM_D), rd = normalize(vec3(sp, -CAM_D));
  float tA = 1e9, tB = -1e9;
  for (int i = 0; i < ${MAX}; i++) {
    float R = BOUND * uBScale[i] * 1.06;
    vec3 oc = ro - uBPos[i];
    float b = dot(oc, rd), h = b * b - (dot(oc, oc) - R * R);
    if (h > 0.0) { h = sqrt(h); tA = min(tA, -b - h); tB = max(tB, -b + h); }
  }
  if (tB <= tA) { outColor = vec4(0.0); return; }
  float t = max(tA, 0.0), pxk = 2.0 / uRes.y / CAM_D, best = 1e9, tBest = t;
  bool hit = false;
  for (int i = 0; i < 140; i++) {
    float d = map(ro + rd * t);
    float rel = d / (t * pxk);
    if (rel < best) { best = rel; tBest = t; }
    if (d < 0.0004) { hit = true; break; }
    t += d * 0.8;
    if (t > tB) break;
  }
  float cover = hit ? 1.0 : clamp(1.2 - best, 0.0, 1.0);
  if (cover <= 0.0) { outColor = vec4(0.0); return; }
  outColor = vec4(shade(ro + rd * (hit ? t : tBest), rd) * cover, cover);
}`;

  // ---- WebGL setup ----
  function sh(type, src) {
    const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    return s;
  }
  const prog = gl.createProgram();
  try {
    gl.attachShader(prog, sh(gl.VERTEX_SHADER, '#version 300 es\nin vec2 aPos;void main(){gl_Position=vec4(aPos,0.0,1.0);}'));
    gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FRAG));
  } catch (e) { console.warn(e); return; }
  gl.bindAttribLocation(prog, 0, 'aPos');
  gl.linkProgram(prog);
  gl.useProgram(prog);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
  const U = {};
  ['uRes', 'uBPos', 'uBRot', 'uBScale', 'uBg', 'uBgScale', 'uLodBase'].forEach(n => { U[n] = gl.getUniformLocation(prog, n); });

  let bgReady = false, bgW = 16, bgH = 9;
  const tex = gl.createTexture();
  const img = new Image();
  img.onload = () => {
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, img);
    gl.generateMipmap(gl.TEXTURE_2D);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    bgW = img.naturalWidth; bgH = img.naturalHeight; bgReady = true;
  };
  img.src = S.bg;

  function resize() {
    const k = Math.min(window.devicePixelRatio || 1, 1.5);
    let W = Math.round(box.clientWidth * k), H = Math.round(box.clientHeight * k);
    const cap = 2.1e6; // keep big screens affordable
    if (W * H > cap) { const f = Math.sqrt(cap / (W * H)); W = Math.round(W * f); H = Math.round(H * f); }
    if (canvas.width !== W || canvas.height !== H) { canvas.width = W; canvas.height = H; }
  }
  new ResizeObserver(resize).observe(box);
  resize();

  // ---- falling bricks: rigid bodies that bounce off each other ----
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]];
  const add = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]];
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
  function mul(A, B) {
    const C = [[0, 0, 0], [0, 0, 0], [0, 0, 0]];
    for (let i = 0; i < 3; i++) for (let j = 0; j < 3; j++) for (let k = 0; k < 3; k++) C[i][j] += A[i][k] * B[k][j];
    return C;
  }
  function axisAngle(ax, a) {
    const c = Math.cos(a), s = Math.sin(a), t = 1 - c, [x, y, z] = ax;
    return [[t * x * x + c, t * x * y - s * z, t * x * z + s * y], [t * x * y + s * z, t * y * y + c, t * y * z - s * x], [t * x * z - s * y, t * y * z + s * x, t * z * z + c]];
  }
  function randomAxis() {
    const z = Math.random() * 2 - 1, a = Math.random() * Math.PI * 2, r = Math.sqrt(1 - z * z);
    return [r * Math.cos(a), r * Math.sin(a), z];
  }
  const BOUND = Math.hypot(...HALF) + 0.03;
  let bricks = [];
  function spawn(b, yStart) {
    const A = canvas.width / Math.max(1, canvas.height);
    const k = 0.85 + Math.random() * 0.3, r = BOUND * S.size * k;
    const half = Math.max(0, (A - r * 0.6) * S.spread);
    let x = 0, y = yStart != null ? yStart : 1 + r + 0.15 + Math.random() * 0.4;
    for (let i = 0; i < 16; i++) {
      x = (Math.random() * 2 - 1) * half;
      if (!bricks.some(o => o !== b && o.p && Math.hypot(o.p[0] - x, o.p[1] - y) < (o.r + r) * 0.85)) break;
      if (yStart == null && i % 4 === 3) y += r * 0.6;
    }
    const term = (0.75 + Math.random() * 0.5) * 0.6, spin = (50 + Math.random() * 110) * (Math.random() < 0.5 ? -1 : 1) * Math.PI / 180;
    const ax = randomAxis();
    return Object.assign(b, { p: [x, y, (Math.random() * 2 - 1) * 0.35], v: [0, -term, 0], term,
      w: ax.map(c => c * spin), O: axisAngle(randomAxis(), Math.random() * Math.PI * 2), k, r });
  }
  for (let i = 0; i < S.count; i++) bricks.push(spawn({}, 1.25 - (i + 0.2 + Math.random() * 0.6) * (2.6 / S.count)));

  function boxOf(b) { const sc = S.size * b.k; return { c: b.p, u: [0, 1, 2].map(i => [b.O[0][i], b.O[1][i], b.O[2][i]]), e: HALF.map(h => h * sc) }; }
  function overlap(A, B) {
    const axes = [...A.u, ...B.u];
    for (const a of A.u) for (const b of B.u) { const c = cross(a, b), l = Math.hypot(...c); if (l > 1e-4) axes.push(c.map(v => v / l)); }
    const d = sub(B.c, A.c);
    let best = null;
    for (const L of axes) {
      const pen = A.e.reduce((t, e, i) => t + e * Math.abs(dot(A.u[i], L)), 0) + B.e.reduce((t, e, i) => t + e * Math.abs(dot(B.u[i], L)), 0) - Math.abs(dot(d, L));
      if (pen <= 0) return null;
      if (!best || pen < best.pen) best = { pen, n: dot(d, L) < 0 ? L.map(v => -v) : L };
    }
    return best;
  }
  const support = (X, dir) => X.u.reduce((p, u, i) => add(p, u.map(v => v * X.e[i] * Math.sign(dot(u, dir) || 1))), X.c.slice());
  function collide() {
    for (let i = 0; i < bricks.length; i++) for (let j = i + 1; j < bricks.length; j++) {
      const A = bricks[i], B = bricks[j];
      if (Math.hypot(...sub(A.p, B.p)) > A.r + B.r) continue;
      const bA = boxOf(A), bB = boxOf(B), hit = overlap(bA, bB);
      if (!hit) continue;
      const n = hit.n, pa = support(bA, n), pb = support(bB, n.map(v => -v));
      const P = pa.map((c, k) => (c + pb[k]) / 2), rA = sub(P, A.p), rB = sub(P, B.p);
      const sa = S.size * A.k, sb = S.size * B.k, mA = A.k ** 3, mB = B.k ** 3, IA = mA * 0.35 * sa * sa, IB = mB * 0.35 * sb * sb;
      const vn = dot(sub(add(B.v, cross(B.w, rB)), add(A.v, cross(A.w, rA))), n);
      if (vn < 0) {
        const cA = cross(rA, n), cB = cross(rB, n);
        const imp = -1.35 * vn / (1 / mA + 1 / mB + dot(cA, cA) / IA + dot(cB, cB) / IB);
        for (let k = 0; k < 3; k++) { A.v[k] -= imp * n[k] / mA; B.v[k] += imp * n[k] / mB; A.w[k] -= cA[k] * imp / IA; B.w[k] += cB[k] * imp / IB; }
      }
      const corr = hit.pen * 0.9 + 0.002;
      for (let k = 0; k < 3; k++) { A.p[k] -= n[k] * corr * mB / (mA + mB); B.p[k] += n[k] * corr * mA / (mA + mB); }
    }
  }
  function orthonormalize(M) {
    let x = [M[0][0], M[1][0], M[2][0]], y = [M[0][1], M[1][1], M[2][1]];
    const lx = Math.hypot(...x); x = x.map(c => c / lx);
    const d = dot(x, y); y = y.map((c, i) => c - d * x[i]);
    const ly = Math.hypot(...y); y = y.map(c => c / ly);
    const z = cross(x, y);
    for (let i = 0; i < 3; i++) { M[i][0] = x[i]; M[i][1] = y[i]; M[i][2] = z[i]; }
  }
  function step(dt) {
    const T = dt * S.speed / 0.1, n = Math.max(1, Math.ceil(T / 0.012)), h = T / n;
    for (let it = 0; it < n; it++) {
      for (const b of bricks) {
        b.v[1] += (-b.term - b.v[1]) * Math.min(1, h * 1.2);
        const drag = Math.exp(-0.6 * h); b.v[0] *= drag; b.v[2] *= drag;
        b.v[2] -= b.p[2] * 1.5 * h;
        for (let k = 0; k < 3; k++) b.p[k] += b.v[k] * h;
        let wl = Math.hypot(...b.w);
        if (wl > 6) { b.w = b.w.map(c => c * 6 / wl); wl = 6; }
        if (wl > 1e-6) b.O = mul(axisAngle(b.w.map(c => c / wl), wl * h), b.O);
      }
      collide();
    }
    for (const b of bricks) { orthonormalize(b.O); if (b.p[1] < -1 - b.r - 0.15) spawn(b, null); }
  }

  // ---- render loop: runs only while the block is on screen ----
  function draw() {
    const W = canvas.width, H = canvas.height;
    gl.viewport(0, 0, W, H);
    gl.clearColor(0, 0, 0, 0);
    gl.clear(gl.COLOR_BUFFER_BIT);
    if (!bgReady) return;
    const pos = new Float32Array(MAX * 3), rot = new Float32Array(MAX * 9), scl = new Float32Array(MAX);
    bricks.forEach((b, i) => {
      pos.set(b.p, i * 3);
      rot.set([b.O[0][0], b.O[0][1], b.O[0][2], b.O[1][0], b.O[1][1], b.O[1][2], b.O[2][0], b.O[2][1], b.O[2][2]], i * 9);
      scl[i] = S.size * b.k;
    });
    gl.uniform2f(U.uRes, W, H);
    gl.uniform3fv(U.uBPos, pos);
    gl.uniformMatrix3fv(U.uBRot, false, rot);
    gl.uniform1fv(U.uBScale, scl);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.uniform1i(U.uBg, 0);
    const A = W / H, T = bgW / bgH;
    const sx = A > T ? 1 : A / T, sy = A > T ? T / A : 1;
    gl.uniform2f(U.uBgScale, sx, sy);
    gl.uniform1f(U.uLodBase, Math.max(0, Math.log2(bgH * sy / H)));
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
  const still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  let visible = true, raf = 0, last = 0;
  function frame(now) {
    raf = 0;
    const dt = last ? Math.min(0.05, (now - last) / 1000) : 0;
    last = now;
    if (!still) step(dt);
    draw();
    if (visible && !still && !document.hidden) raf = requestAnimationFrame(frame);
  }
  function wake() { if (!raf && visible && !document.hidden) { last = 0; raf = requestAnimationFrame(frame); } }
  new IntersectionObserver(es => { visible = es[0].isIntersecting; wake(); }).observe(box);
  document.addEventListener('visibilitychange', wake);
  img.addEventListener('load', () => { if (!raf) { last = 0; raf = requestAnimationFrame(frame); } });
})();
