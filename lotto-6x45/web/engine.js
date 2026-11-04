/* «6 из 45»: the same method as gosloto645.py, in JavaScript (browser and Node). */
(function (root) {
  'use strict';

  // ---------------------------------------------------------------- math helpers
  function comb(n, k) {
    if (k < 0 || k > n) return 0;
    let r = 1;
    for (let i = 1; i <= k; i++) r = (r * (n - k + i)) / i;
    return r;
  }
  // P(exactly k of the 6 drawn numbers are on one ticket)
  const H = [];
  for (let k = 0; k <= 6; k++) H[k] = (comb(6, k) * comb(39, 6 - k)) / comb(45, 6);

  function lgamma(z) {
    const c = [0.99999999999980993, 676.5203681218851, -1259.1392167224028, 771.32342877765313,
      -176.61502916214059, 12.507343278686905, -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7];
    if (z < 0.5) return Math.log(Math.PI / Math.sin(Math.PI * z)) - lgamma(1 - z);
    z -= 1;
    let x = c[0];
    for (let i = 1; i < 9; i++) x += c[i] / (z + i);
    const t = z + 7.5;
    return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
  }

  // upper tail of the chi-square distribution
  function chi2sf(x, k) {
    const a = k / 2;
    x = x / 2;
    if (x <= 0) return 1;
    const lg = lgamma(a);
    if (x < a + 1) {
      let s = 1 / a, t = 1 / a, n = a;
      for (let i = 0; i < 2000; i++) {
        n += 1; t *= x / n; s += t;
        if (Math.abs(t) < 1e-15 * s) break;
      }
      return Math.max(0, 1 - s * Math.exp(-x + a * Math.log(x) - lg));
    }
    let b = x + 1 - a, c = 1e300, d = 1 / b, h = d;
    for (let i = 1; i < 2000; i++) {
      const an = -i * (i - a);
      b += 2; d = an * d + b; d = d ? 1 / d : 1e300; c = b + an / c; h *= d * c;
      if (Math.abs(d * c - 1) < 1e-15) break;
    }
    return Math.exp(-x + a * Math.log(x) - lg) * h;
  }

  // Gaussian elimination with partial pivoting
  function solve(A, b) {
    const n = b.length;
    const M = A.map((row, i) => row.concat([b[i]]));
    for (let c = 0; c < n; c++) {
      let p = c;
      for (let r = c + 1; r < n; r++) if (Math.abs(M[r][c]) > Math.abs(M[p][c])) p = r;
      const tmp = M[c]; M[c] = M[p]; M[p] = tmp;
      const piv = M[c][c];
      if (Math.abs(piv) < 1e-12) continue;
      for (let r = c + 1; r < n; r++) {
        const f = M[r][c] / piv;
        if (!f) continue;
        const row = M[r], top = M[c];
        for (let j = c; j <= n; j++) row[j] -= f * top[j];
      }
    }
    const x = new Array(n).fill(0);
    for (let i = n - 1; i >= 0; i--) {
      let s = M[i][n];
      for (let j = i + 1; j < n; j++) s -= M[i][j] * x[j];
      x[i] = Math.abs(M[i][i]) > 1e-12 ? s / M[i][i] : 0;
    }
    return x;
  }

  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6D2B79F5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function sampleFrom(pool, k, rng) {
    const a = pool.slice();
    for (let i = 0; i < k; i++) {
      const j = i + Math.floor(rng() * (a.length - i));
      const t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a.slice(0, k).sort((x, y) => x - y);
  }
  const ALL = Array.from({ length: 45 }, (_, i) => i + 1);
  const sample6 = (rng) => sampleFrom(ALL, 6, rng);

  // ---------------------------------------------------------------- data
  // compact row: [number, "YYYY-MM-DD HH:MM", b1..b6, columns, price, superprize, w2, w3, w4, w5, d2, d3, d4, d5]
  function parseDraws(rows) {
    return rows.map((r) => {
      const balls = r.slice(2, 8);
      const s = balls.slice().sort((x, y) => x - y);
      const f = [0, 0, 0, 0];
      for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) {
        const q = pairFeatures(s[i], s[j]);
        for (let t = 0; t < 4; t++) f[t] += q[t];
      }
      return {
        n: r[0], date: r[1], balls, sorted: s, idx: s.map((x) => x - 1), f,
        N: r[8] || 0, price: r[9] || 0, sp: r[10] || 0,
        w: [null, null, r[11], r[12], r[13], r[14]],
        d: [null, null, r[15], r[16], r[17], r[18]],
      };
    });
  }

  // ---------------------------------------------------------------- 1. are the draws random?
  function randomnessReport(draws) {
    const T = draws.length;
    const cnt = new Array(46).fill(0);
    for (const d of draws) for (const x of d.balls) cnt[x]++;
    const E = (T * 6) / 45, fpc = (45 - 6) / (45 - 1);
    let chi = 0;
    for (let i = 1; i <= 45; i++) chi += ((cnt[i] - E) ** 2) / E;
    const out = { draws: T, freqP: chi2sf(chi / fpc, 44), minCount: Math.min(...cnt.slice(1)), maxCount: Math.max(...cnt.slice(1)), expected: E };
    out.posP = [];
    for (let pos = 0; pos < 6; pos++) {
      const c = new Array(46).fill(0);
      for (const d of draws) c[d.balls[pos]]++;
      const e = T / 45;
      let x = 0;
      for (let i = 1; i <= 45; i++) x += ((c[i] - e) ** 2) / e;
      out.posP.push(chi2sf(x, 44));
    }
    const pc = new Int32Array(46 * 46);
    for (const d of draws) {
      const s = d.sorted;
      for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) pc[s[i] * 46 + s[j]]++;
    }
    const ep = (T * 15) / 990;
    let xp = 0;
    for (let a = 1; a <= 45; a++) for (let b = a + 1; b <= 45; b++) xp += ((pc[a * 46 + b] - ep) ** 2) / ep;
    out.pairsP = chi2sf(xp, 989);
    const ov = [];
    for (let i = 1; i < T; i++) {
      const prev = new Set(draws[i - 1].balls);
      let k = 0;
      for (const x of draws[i].balls) if (prev.has(x)) k++;
      ov.push(k);
    }
    const m = ov.reduce((s, v) => s + v, 0) / ov.length;
    const sd = Math.sqrt(ov.reduce((s, v) => s + (v - m) ** 2, 0) / ov.length);
    out.overlapMean = m;
    out.overlapZ = (m - 0.8) / (sd / Math.sqrt(ov.length));
    return out;
  }

  // Prequential check of frequency forecasts: each draw is forecast only from the draws before it.
  // A positive total score would be a real, exploitable bias; then p follows that forecast.
  function biasModel(draws, gate = 10) {
    let best = null;
    const table = [];
    for (const hl of [300, 1000, 3000, null]) {
      const dec = hl ? Math.pow(0.5, 1 / hl) : 1;
      for (const a of [450, 4500]) {
        const c = new Float64Array(46);
        let n = 0, score = 0;
        draws.forEach((d, t) => {
          if (t >= 200) for (const x of d.balls) score += Math.log((45 * (c[x] + a / 45)) / (n + a));
          if (dec !== 1) { for (let i = 1; i <= 45; i++) c[i] *= dec; n *= dec; }
          for (const x of d.balls) c[x] += 1;
          n += 6;
        });
        const p = [0];
        for (let i = 1; i <= 45; i++) p.push((c[i] + a / 45) / (n + a));
        table.push({ hl, a, score });
        if (!best || score > best.score) best = { hl, a, score, p };
      }
    }
    const passed = best.score > gate;
    const uniform = [0].concat(new Array(45).fill(1 / 45));
    return { p: passed ? best.p : uniform, passed, best: { hl: best.hl, a: best.a, score: best.score }, table };
  }

  // ---------------------------------------------------------------- 2. what does the crowd play?
  function pairFeatures(a, b) { // a < b: consecutive, same ten, same last digit, same column of a 9-wide grid
    return [b - a === 1 ? 1 : 0, Math.floor(a / 10) === Math.floor(b / 10) ? 1 : 0, a % 10 === b % 10 ? 1 : 0, (b - a) % 9 === 0 ? 1 : 0];
  }
  const CROWD = { 2: [1500, 0.003], 3: [1500, 0.012], 4: [4000, 0.05] }; // memory half-life in draws, noise floor
  const NF = 50; // 45 numbers, 4 pair features, intercept

  class CrowdFit {
    constructor(draws, k) {
      this.draws = draws; this.k = k;
      [this.hl, this.floor] = CROWD[k];
      this.A = new Float64Array(NF * NF);
      this.b = new Float64Array(NF);
      this.pos = 0;
    }
    advance(end) {
      const k = this.k;
      const shrink = Math.pow(0.5, (end - this.pos) / this.hl);
      if (shrink !== 1) { for (let i = 0; i < NF * NF; i++) this.A[i] *= shrink; for (let i = 0; i < NF; i++) this.b[i] *= shrink; }
      const ent = new Int32Array(11), val = new Float64Array(11);
      for (let t = this.pos; t < end; t++) {
        const d = this.draws[t];
        const W = d.w[k], N = d.N;
        if (W === null || W === undefined || N <= 0) continue;
        const e = N * H[k];
        const y = Math.log((W + 0.5) / e);
        const w = Math.pow(0.5, (end - 1 - t) / this.hl) / (1 / e + this.floor);
        let m = 0;
        for (const i of d.idx) { ent[m] = i; val[m] = 1; m++; }
        for (let i = 0; i < 4; i++) if (d.f[i]) { ent[m] = 45 + i; val[m] = d.f[i]; m++; }
        ent[m] = NF - 1; val[m] = 1; m++;
        for (let x = 0; x < m; x++) {
          const j = ent[x], wv = w * val[x], row = j * NF;
          for (let z = 0; z < m; z++) this.A[row + ent[z]] += wv * val[z];
          this.b[j] += wv * y;
        }
      }
      this.pos = end;
    }
    solve() {
      const A = [];
      for (let i = 0; i < NF; i++) A.push(Array.from(this.A.subarray(i * NF, (i + 1) * NF)));
      for (let j = 0; j < 45; j++) A[j][j] += 50;
      for (let j = 45; j < 49; j++) A[j][j] += 0.5;
      const sol = solve(A, Array.from(this.b));
      return { beta: sol.slice(0, 45), theta: sol.slice(45, 49), mu: sol[49] };
    }
  }

  // Scores a ticket: how much more (or less) it is expected to pay per hit than an average ticket.
  class Crowd {
    constructor(coefs, p, nNorm = 3000, seed = 7) {
      this.coefs = coefs;
      p = p || [0].concat(new Array(45).fill(1 / 45));
      this.e = {}; this.q = {}; this.beta = {};
      for (const k of Object.keys(coefs).map(Number)) {
        const { beta, theta } = coefs[k];
        const b = [0].concat(beta);
        this.beta[k] = b;
        const e = new Float64Array(46);
        for (let i = 1; i <= 45; i++) e[i] = 45 * p[i] * Math.exp(-b[i]); // chance factor × crowd factor
        const q = new Float64Array(46 * 46).fill(1);
        for (let a = 1; a <= 45; a++) for (let c = a + 1; c <= 45; c++) {
          const f = pairFeatures(a, c);
          const v = Math.exp(-(theta[0] * f[0] + theta[1] * f[1] + theta[2] * f[2] + theta[3] * f[3]));
          q[a * 46 + c] = v; q[c * 46 + a] = v;
        }
        this.e[k] = e; this.q[k] = q;
      }
      this.tiers = Object.keys(coefs).map(Number);
      // How often the crowd plays a whole six. A drawn number shifts log(winners) of tier k by about
      // (k/6 - (6-k)/39) times its pick-rate effect, and a pair pattern by k(k-1)/30 of its effect;
      // inverting that for tiers 2 and 3 gives the crowd's own number and pattern preferences.
      this.p6 = new Float64Array(46);
      this.q6 = new Float64Array(46 * 46).fill(1);
      if (coefs[2] && coefs[3]) {
        for (let i = 1; i <= 45; i++) this.p6[i] = Math.exp((coefs[2].beta[i - 1] / 0.23077 + coefs[3].beta[i - 1] / 0.42308) / 2);
        const phi = [0, 1, 2, 3].map((j) => (15 * coefs[2].theta[j] + 5 * coefs[3].theta[j]) / 2);
        for (let a = 1; a <= 45; a++) for (let c = a + 1; c <= 45; c++) {
          const f = pairFeatures(a, c);
          const v = Math.exp(phi[0] * f[0] + phi[1] * f[1] + phi[2] * f[2] + phi[3] * f[3]);
          this.q6[a * 46 + c] = v; this.q6[c * 46 + a] = v;
        }
      } else {
        this.p6.fill(1);
      }
      this.norm = {};
      for (const k of this.tiers) this.norm[k] = 1;
      this.norm6 = 1;
      const rng = mulberry32(seed), acc = {};
      for (const k of this.tiers) acc[k] = 0;
      let acc6 = 0;
      for (let i = 0; i < nNorm; i++) {
        const C = sample6(rng);
        const g = this.raw(C);
        for (const k of this.tiers) acc[k] += g[k];
        acc6 += this.pop6(C);
      }
      for (const k of this.tiers) this.norm[k] = acc[k] / nNorm;
      this.norm6 = acc6 / nNorm;
    }
    pop6(C) {
      let v = 1;
      for (let i = 0; i < 6; i++) {
        v *= this.p6[C[i]];
        for (let j = i + 1; j < 6; j++) v *= this.q6[C[i] * 46 + C[j]];
      }
      return v;
    }
    // how many times more (or less) often than an average ticket the crowd plays exactly these six numbers
    popRel(C) { return this.pop6(C) / this.norm6; }
    // chance that at least one other bet in a draw of `columns` bets has the same six numbers
    shareChance(C, columns) { return 1 - Math.exp(-columns * H[6] * this.popRel(C)); }
    raw(C) {
      const out = {};
      for (const k of this.tiers) {
        const e = this.e[k], q = this.q[k], b = this.beta[k];
        let sb = 0;
        for (const x of C) sb += b[x];
        const rest = Math.exp(((6 - k) / 39) * sb); // the other drawn numbers come from outside the ticket
        let s = 0;
        if (k === 2) {
          for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) s += e[C[i]] * e[C[j]] * q[C[i] * 46 + C[j]];
          s /= 15;
        } else if (k === 3) {
          for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) {
            const ij = e[C[i]] * e[C[j]] * q[C[i] * 46 + C[j]];
            for (let l = j + 1; l < 6; l++) s += ij * e[C[l]] * q[C[i] * 46 + C[l]] * q[C[j] * 46 + C[l]];
          }
          s /= 20;
        } else {
          for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) {
            const ij = e[C[i]] * e[C[j]] * q[C[i] * 46 + C[j]];
            for (let l = j + 1; l < 6; l++) {
              const ijl = ij * e[C[l]] * q[C[i] * 46 + C[l]] * q[C[j] * 46 + C[l]];
              for (let m = l + 1; m < 6; m++) s += ijl * e[C[m]] * q[C[i] * 46 + C[m]] * q[C[j] * 46 + C[m]] * q[C[l] * 46 + C[m]];
            }
          }
          s /= 15;
        }
        out[k] = s * rest;
      }
      return out;
    }
    mult(C) {
      const g = this.raw(C), out = {};
      for (const k of this.tiers) out[k] = g[k] / this.norm[k];
      return out;
    }
  }

  function fitCrowd(draws, end, p, fits) {
    end = end === undefined || end === null ? draws.length : end;
    fits = fits || { 2: new CrowdFit(draws, 2), 3: new CrowdFit(draws, 3), 4: new CrowdFit(draws, 4) };
    const coefs = {};
    for (const k of [2, 3, 4]) { fits[k].advance(end); coefs[k] = fits[k].solve(); }
    return { crowd: new Crowd(coefs, p), fits };
  }

  // ---------------------------------------------------------------- 3. how the prize fund pays right now
  function prizeRegime(draws, windowSize = 14 * 24) {
    const sig = (d) => [2, 3, 4, 5].filter((k) => d.w[k] !== null && d.w[k] !== undefined).join(',') + '|' + d.price;
    const last = sig(draws[draws.length - 1]);
    let start = draws.length - 1;
    while (start > 0 && sig(draws[start - 1]) === last) start--;
    const reg = draws.slice(Math.max(start, draws.length - windowSize)).filter((d) => d.N > 0);
    const lastDraw = draws[draws.length - 1];
    const info = { startNumber: draws[start].n, draws: reg.length, price: lastDraw.price, superprize: lastDraw.sp, tiers: {}, slots: {} };
    for (const k of [2, 3, 4, 5]) {
      const vals = reg.filter((d) => d.w[k] && d.d[k]).map((d) => d.d[k]);
      if (!vals.length) continue;
      const distinct = new Set(vals).size / vals.length;
      const mean = vals.reduce((s, v) => s + v, 0) / vals.length;
      const cv = mean ? Math.sqrt(vals.reduce((s, v) => s + (v - mean) ** 2, 0) / vals.length) / mean : 0;
      const shared = distinct > 0.5 && cv > 0.05;
      const fixed = vals.slice().sort((x, y) => x - y)[Math.floor(vals.length / 2)];
      // a shared tier's fund in one draw = fixed part + a share of every bet
      const xs = reg.map((d) => d.N), ys = reg.map((d) => (d.w[k] || 0) * (d.d[k] || 0));
      const mx = xs.reduce((s, v) => s + v, 0) / xs.length, my = ys.reduce((s, v) => s + v, 0) / ys.length;
      let sxx = 0, sxy = 0;
      xs.forEach((x, i) => { sxx += (x - mx) ** 2; sxy += (x - mx) * (ys[i] - my); });
      let b = sxx ? sxy / sxx : 0, a = my - b * mx;
      const perCol = xs.reduce((s, x, i) => s + ys[i] / x, 0) / xs.length;
      if (!shared || reg.length < 8 || a < 0 || b < 0) { a = 0; b = perCol; }
      info.tiers[k] = { shared, fixed, perCol, a, b };
    }
    const ns = reg.map((d) => d.N).sort((x, y) => x - y);
    info.nMedian = ns.length ? ns[Math.floor(ns.length / 2)] : 0;
    info.endNumber = lastDraw.n;
    // boost: shared tiers carry a fixed sum on top of the bets (an accumulated fund being paid out);
    // shared: prizes split between winners only; fixed: fixed prizes and an accumulating superprize
    let fixedPart = 0, total = 0, evRest = 0;
    for (const k of Object.keys(info.tiers).map(Number)) {
      const t = info.tiers[k];
      if (t.shared) {
        fixedPart += t.a; total += t.a + t.b * info.nMedian;
        evRest += info.nMedian ? (t.a + t.b * info.nMedian) / info.nMedian : t.perCol;
      } else {
        evRest += H[k] * t.fixed;
      }
    }
    const sharedTiers = Object.keys(info.tiers).filter((k) => info.tiers[k].shared);
    info.mode = !sharedTiers.length ? 'fixed' : total > 0 && fixedPart / total > 0.15 ? 'boost' : 'shared';
    info.evRest = evRest;
    info.breakEven = Math.max(0, (info.price - evRest) / H[6]); // superprize at which an average bet pays back
    const bySlot = {};
    for (const d of reg) (bySlot[d.date.slice(11, 16)] = bySlot[d.date.slice(11, 16)] || []).push(d);
    for (const s of Object.keys(bySlot).sort()) {
      const ds = bySlot[s].slice(-10);
      const cols = ds.map((d) => d.N).sort((x, y) => x - y);
      info.slots[s] = { columns: cols[Math.floor(cols.length / 2)], draws: bySlot[s].length };
    }
    return info;
  }

  // expected return of one bet in a draw with `columns` bets: [average ticket, this ticket]
  function ticketValue(info, mult, columns) {
    let avg = H[6] * info.superprize, our = avg;
    for (const k of Object.keys(info.tiers).map(Number)) {
      const t = info.tiers[k];
      if (t.shared) {
        const ev = (t.a + t.b * columns) / columns;
        avg += ev;
        our += ev * (mult[k] || 1);
      } else {
        avg += H[k] * t.fixed;
        our += H[k] * t.fixed;
      }
    }
    return [avg, our];
  }

  // the rules that were in force before the current ones (what the game returns to when a payout campaign ends)
  function previousRegime(draws) {
    const cur = prizeRegime(draws);
    const idx = draws.findIndex((d) => d.n === cur.startNumber);
    if (idx <= 0) return null;
    const prev = prizeRegime(draws.slice(0, idx));
    prev.endNumber = draws[idx - 1].n;
    return prev;
  }

  // ---------------------------------------------------------------- 4. choosing tickets
  // skip shapes that pattern players fill in by hand: they make prizes shared more often
  function acceptable(C, recent) {
    let run = 1, best = 1;
    for (let i = 1; i < 6; i++) { run = C[i] - C[i - 1] === 1 ? run + 1 : 1; if (run > best) best = run; }
    if (best >= 3) return false;
    const tens = [0, 0, 0, 0, 0];
    for (const x of C) tens[Math.floor(x / 10)]++;
    if (Math.max(...tens) >= 4) return false;
    for (const w of [7, 8, 9, 10]) {
      const cols = new Array(w).fill(0);
      for (const x of C) cols[(x - 1) % w]++;
      if (Math.max(...cols) >= 4) return false;
    }
    const ss = new Set(C);
    for (let i = 0; i < 6; i++) for (let j = i + 1; j < 6; j++) {
      const a = C[i], st = C[j] - C[i];
      if (ss.has(a + 2 * st) && ss.has(a + 3 * st)) return false;
    }
    for (const r of recent) {
      let k = 0;
      for (const x of C) if (r.has(x)) k++;
      if (k >= 4) return false;
    }
    return true;
  }

  function shared(A, B) { let k = 0; for (const x of A) if (B.includes(x)) k++; return k; }

  // local search over 6-number tickets maximizing `score`; tickets share at most `maxShared` numbers
  function pickTickets(score, n, recent, rng, restarts = 6, maxShared = 2) {
    const chosen = [];
    for (let t = 0; t < n; t++) {
      let bestC = null, bestS = -Infinity;
      for (let r = 0; r < restarts; r++) {
        let C = null;
        for (let tr = 0; tr < 200; tr++) {
          const c = sample6(rng);
          if (acceptable(c, recent) && chosen.every((o) => shared(c, o) <= maxShared)) { C = c; break; }
        }
        if (!C) continue;
        let cur = score(C), improved = true;
        while (improved) {
          improved = false;
          let candS = cur, candC = null;
          for (let i = 0; i < 6; i++) {
            const rest = C.slice(0, i).concat(C.slice(i + 1));
            for (let x = 1; x <= 45; x++) {
              if (C.includes(x)) continue;
              const C2 = rest.concat([x]).sort((a, b) => a - b);
              if (!acceptable(C2, recent) || chosen.some((o) => shared(C2, o) > maxShared)) continue;
              const s = score(C2);
              if (s > candS + 1e-12) { candS = s; candC = C2; }
            }
          }
          if (candC) { C = candC; cur = candS; improved = true; }
        }
        if (cur > bestS) { bestC = C; bestS = cur; }
      }
      if (bestC) chosen.push(bestC);
    }
    return chosen;
  }

  const objective = (crowd, weights) => (C) => {
    const m = crowd.mult(C);
    let s = 0;
    for (const k of Object.keys(weights)) s += weights[k] * m[k];
    return s;
  };

  // how much each shared tier contributes to a ticket's value under the current rules
  function tierWeights(info) {
    const w = {};
    for (const k of [2, 3, 4]) if (info.tiers[k] && info.tiers[k].shared) w[k] = info.tiers[k].perCol;
    return Object.keys(w).length ? w : { 2: 0.2, 3: 0.3, 4: 0.5 };
  }

  // shared prizes: maximize the expected prize per hit; fixed prizes: only the superprize can be split,
  // so pick the six numbers the fewest other people play
  function strategyObjective(crowd, info) {
    if (info.mode === 'fixed') return (C) => -Math.log(crowd.popRel(C));
    return objective(crowd, tierWeights(info));
  }

  // how large the superprize has been lately: the yardstick for the break-even level under fixed prizes
  function superprizeStats(draws) {
    const last = draws[draws.length - 1];
    const t = Date.parse(last.date.slice(0, 10));
    const within = (days) => draws.filter((d) => d.sp > 0 && t - Date.parse(d.date.slice(0, 10)) <= days * 864e5).map((d) => d.sp);
    const y3 = within(3 * 365), y1 = within(365).sort((a, b) => a - b);
    return { last: last.sp, max3y: y3.reduce((m, v) => (v > m ? v : m), 0), median1y: y1.length ? y1[Math.floor(y1.length / 2)] : 0 };
  }

  // ---------------------------------------------------------------- everything for the next draw
  function analyze(draws, opts = {}) {
    const randomness = randomnessReport(draws);
    const bias = biasModel(draws);
    const { crowd } = fitCrowd(draws, draws.length, bias.p);
    const info = prizeRegime(draws);
    const recent = draws.slice(-50).map((d) => d.balls.slice());
    const last = draws[draws.length - 1];
    const model = { coefs: crowd.coefs, p: bias.p, recent, info, prev: previousRegime(draws) };
    return {
      status: {
        count: draws.length, first: { n: draws[0].n, date: draws[0].date }, last: { n: last.n, date: last.date, balls: last.sorted },
        superprize: superprizeStats(draws),
      },
      randomness, bias: { passed: bias.passed, best: bias.best }, model,
      tickets: chooseTickets(model, opts.tickets || 10, opts.seed || last.n),
    };
  }

  function crowdFromModel(model) { return new Crowd(model.coefs, model.p); }

  function chooseTickets(model, n, seed, crowd) {
    crowd = crowd || crowdFromModel(model);
    const recent = model.recent.map((b) => new Set(b));
    const rng = mulberry32(seed);
    const list = pickTickets(strategyObjective(crowd, model.info), n, recent, rng, n > 10 ? 2 : 6, n > 20 ? 3 : 2);
    return list.map((C) => ({ C, mult: crowd.mult(C), popRel: crowd.popRel(C) }));
  }

  // ---------------------------------------------------------------- walk-forward test on past draws
  async function backtest(draws, opts = {}, onProgress) {
    const start = opts.start || 5000, block = opts.block || 1000, k = opts.k || 10;
    const rng = mulberry32(opts.seed || 1);
    // payouts are recomputed with the latest rules under which prizes were split between winners
    let info = prizeRegime(draws), cut = draws.length;
    for (let guard = 0; guard < 12 && info.mode === 'fixed'; guard++) {
      cut = draws.findIndex((d) => d.n === info.startNumber);
      if (cut <= 0) break;
      info = prizeRegime(draws.slice(0, cut));
    }
    const weights = tierWeights(info);
    const A = {};
    for (const m of [2, 3, 4]) if (info.tiers[m] && info.tiers[m].shared) A[m] = info.tiers[m].perCol / H[m]; // prize per expected winner
    if (!Object.keys(A).length) { A[2] = 180; A[3] = 750; A[4] = 4400; }
    const names = ['anti', 'random', 'popular', 'hot', 'cold'];
    const blocks = [];
    let fits = null;
    const nBlocks = Math.ceil((draws.length - start) / block);
    for (let b0 = start, bi = 0; b0 < draws.length; b0 += block, bi++) {
      const fc = fitCrowd(draws, b0, null, fits);
      fits = fc.fits;
      const crowd = fc.crowd;
      const recent = draws.slice(Math.max(0, b0 - 50), b0).map((d) => new Set(d.balls));
      const obj = objective(crowd, weights);
      const anti = pickTickets(obj, k, recent, rng, 2);
      const popular = pickTickets((C) => -obj(C), k, [], rng, 2);
      const rnd = Array.from({ length: k }, () => sample6(rng));
      const freq = new Array(46).fill(0);
      for (const d of draws.slice(Math.max(0, b0 - 300), b0)) for (const x of d.balls) freq[x]++;
      const order = ALL.slice().sort((a, b) => freq[b] - freq[a]);
      const hot = Array.from({ length: k }, () => sampleFrom(order.slice(0, 12), 6, rng));
      const cold = Array.from({ length: k }, () => sampleFrom(order.slice(-12), 6, rng));
      const sets = { anti, random: rnd, popular, hot, cold };
      const st = {};
      for (const s of names) st[s] = { hits: [0, 0, 0, 0, 0, 0, 0], rel: { 2: [0, 0], 3: [0, 0], 4: [0, 0] }, sim: [0, 0], real: [0, 0] };
      for (let t = b0; t < Math.min(draws.length, b0 + block); t++) {
        const d = draws[t];
        const D = new Set(d.balls);
        const full = d.N > 0 && [2, 3, 4].every((m) => d.w[m] !== null && d.w[m] !== undefined);
        for (const s of names) {
          const x = st[s];
          for (const C of sets[s]) {
            let m = 0;
            for (const v of C) if (D.has(v)) m++;
            x.hits[m]++;
            if (full) {
              if (A[m] !== undefined) {
                const r = (d.N * H[m]) / (d.w[m] + 1);
                x.sim[0] += A[m] * r;
                x.rel[m][0] += r; x.rel[m][1] += 1;
              }
              x.sim[1] += 1;
            }
            if (m >= 2 && m <= 5 && d.d[m] !== null && d.d[m] !== undefined) x.real[0] += d.d[m];
            x.real[1] += 1;
          }
        }
      }
      blocks.push(st);
      if (onProgress) onProgress(bi + 1, nBlocks, draws[b0].n, anti[0]);
      await new Promise((r) => setTimeout(r, 0));
    }
    const agg = (bl, s) => {
      const hits = [0, 1, 2, 3, 4, 5, 6].map((m) => bl.reduce((t, b) => t + b[s].hits[m], 0));
      const rel = {};
      for (const m of [2, 3, 4]) rel[m] = [bl.reduce((t, b) => t + b[s].rel[m][0], 0), bl.reduce((t, b) => t + b[s].rel[m][1], 0)];
      const sim = bl.reduce((t, b) => t + b[s].sim[0], 0) / Math.max(1, bl.reduce((t, b) => t + b[s].sim[1], 0));
      const real = bl.reduce((t, b) => t + b[s].real[0], 0) / Math.max(1, bl.reduce((t, b) => t + b[s].real[1], 0));
      let size = 0; // prize size only, hits at the theoretical rate
      for (const m of Object.keys(A).map(Number)) size += H[m] * A[m] * (rel[m][0] / Math.max(1, rel[m][1]));
      return { hits, rel, sim, real, size };
    };
    const ci = (key, s) => {
      const r = mulberry32(3), L = blocks.length, vals = [];
      for (let i = 0; i < 1000; i++) {
        const bl = Array.from({ length: L }, () => blocks[Math.floor(r() * L)]);
        const a = agg(bl, s)[key], b = agg(bl, 'random')[key];
        vals.push(b ? a / b : 0);
      }
      vals.sort((x, y) => x - y);
      return [vals[25], vals[974]];
    };
    const res = { from: draws[start].n, to: draws[draws.length - 1].n, draws: draws.length - start, k, block, strategies: {} };
    const base = agg(blocks, 'random');
    for (const s of names) {
      const a = agg(blocks, s);
      const n = a.hits.reduce((t, v) => t + v, 0);
      res.strategies[s] = {
        hitRate: [2, 3, 4, 5].map((m) => a.hits[m] / n),
        prize: [2, 3, 4].map((m) => a.rel[m][0] / Math.max(1, a.rel[m][1])),
        size: a.size, sizeRatio: a.size / base.size, sizeCI: s === 'random' ? [1, 1] : ci('size', s),
        sim: a.sim, simRatio: a.sim / base.sim, simCI: s === 'random' ? [1, 1] : ci('sim', s),
        real: a.real, realRatio: a.real / base.real, realCI: s === 'random' ? [1, 1] : ci('real', s),
      };
    }
    res.theory = [2, 3, 4, 5].map((m) => H[m]);
    return res;
  }

  const api = { H, comb, chi2sf, solve, mulberry32, sample6, parseDraws, randomnessReport, biasModel, pairFeatures,
    CrowdFit, Crowd, fitCrowd, prizeRegime, previousRegime, ticketValue, acceptable, pickTickets, objective, tierWeights,
    strategyObjective, analyze, crowdFromModel, chooseTickets, backtest };
  root.Lotto = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof self !== 'undefined' ? self : globalThis);
