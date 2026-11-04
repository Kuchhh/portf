#!/usr/bin/env node
/* Builds the web version: draws.json from the archive, precomputed results, and index.html.
   Usage: node web/build.js            (after `python gosloto645.py update`) */
'use strict';
const fs = require('fs');
const path = require('path');
const Lotto = require('./engine.js');

const WEB = __dirname;
const CSV = path.join(WEB, '..', 'draws_6x45.csv');

function readCsv(file) {
  const lines = fs.readFileSync(file, 'utf8').trim().split(/\r?\n/);
  const head = lines.shift().split(',');
  const col = (name) => head.indexOf(name);
  const num = (v) => (v === '' || v === undefined ? null : Number(v));
  return lines.map((line) => {
    const r = line.split(',');
    return [Number(r[col('number')]), r[col('date')]]
      .concat([1, 2, 3, 4, 5, 6].map((i) => Number(r[col('b' + i)])))
      .concat([num(r[col('columns')]) || 0, num(r[col('ticket_price')]) || 0, num(r[col('superprize')]) || 0])
      .concat([2, 3, 4, 5].map((k) => num(r[col('w' + k)])))
      .concat([2, 3, 4, 5].map((k) => num(r[col('d' + k)])));
  }).sort((a, b) => a[0] - b[0]);
}

(async () => {
  const rows = readCsv(CSV);
  fs.writeFileSync(path.join(WEB, 'draws.json'), JSON.stringify({ rows }));
  const draws = Lotto.parseDraws(rows);
  const t0 = Date.now();
  const result = Lotto.analyze(draws, { tickets: 10 });
  const t1 = Date.now();
  const bt = await Lotto.backtest(draws, { start: 5000, block: 1000, k: 10, seed: 1 });
  const t2 = Date.now();
  result.backtest = bt;
  result.built = new Date().toISOString().slice(0, 16).replace('T', ' ');
  process.stderr.write(`analyze ${t1 - t0} ms, backtest ${t2 - t1} ms\n`);
  const engine = fs.readFileSync(path.join(WEB, 'engine.js'), 'utf8');
  const app = fs.readFileSync(path.join(WEB, 'app.html'), 'utf8');
  const html = app
    .replace('/*@ENGINE@*/', () => engine)
    .replace('/*@INIT@*/', () => JSON.stringify(result).replace(/</g, '\\u003c'));
  fs.writeFileSync(path.join(WEB, 'index.html'), html);
  if (process.argv.includes('--print')) console.log(JSON.stringify(result, null, 1));
})();
