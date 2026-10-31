/* Extract calculator JS from the built HTML, run it with a DOM stub, compare to hand values. */
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, 'tools', 'marketplace-fee-calculator.html'), 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>\s*<\/body>/);
if (!m) { console.error('FAIL: script block not found'); process.exit(1); }
const code = m[1];

const els = {};
function el(id) {
  if (!els[id]) {
    els[id] = {
      id, value: '', innerHTML: '', style: {},
      _listeners: {},
      addEventListener(ev, fn) { (this._listeners[ev] = this._listeners[ev] || []).push(fn); },
      querySelector() { return null; },
      fire(ev) { (this._listeners[ev] || []).forEach(fn => fn()); },
    };
  }
  return els[id];
}
['platform','price','shipping','cost','ads','offsite','vol','pct','payPct','payFix','listing','reg','monthly','calcBtn','result','upsell']
  .forEach(id => el(id));

global.document = { getElementById: id => el(id) };
global.window = global;

Object.assign(el('platform'), { value: 'etsy' });
Object.entries({ price: '35', shipping: '5.99', cost: '10', ads: '3', offsite: '15',
                 vol: '50', pct: '6.5', payPct: '3', payFix: '0.25',
                 listing: '0.20', reg: '0.25', monthly: '0' })
  .forEach(([k, v]) => { el(k).value = v; });

try { eval(code); } catch (e) { console.error('FAIL: JS threw:', e.message); process.exit(1); }

const out = el('result').innerHTML;
const upsell = el('upsell').innerHTML;
const text = out.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
console.log(text);

const checks = [
  ['profit 19.57', /19\.57/, out],
  ['buyer pays 40.99', /40\.99/, out],
  ['tx fee 2.27', /2\.27/, out],
  ['processing 1.48', /1\.48/, out],
  ['offsite 6.15', /6\.15/, out],
  ['monthly profit 978.48', /978\.48/, out],
  ['break-even 14.46', /14\.46/, out],
  ['30% margin price', /Price for a 30%/, out],
  ['upsell present', /Profit Tracker/, upsell],
];
let failed = 0;
for (const [label, re, hay] of checks) {
  if (re.test(hay)) { console.log('PASS', label); }
  else { console.log('FAIL', label); failed++; }
}

// independent self-check: at the break-even price (shipping = 0) profit must be 0
const x = { pct: 6.5, payPct: 3, ads: 3, offsite: 15, reg: 0.25, payFix: 0.25, listing: 0.20, cost: 10, shipping: 0 };
const k = 1 - x.pct/100 - x.payPct/100 - x.ads/100 - x.offsite/100 - x.reg/100;
const be = (x.cost + x.payFix + x.listing) / k;
const profitAtBE = (be + x.shipping) * k - x.shipping - (x.payFix + x.listing + x.cost);
const ok = Math.abs(profitAtBE) < 1e-9;
console.log(ok ? 'PASS break-even self-consistent' : 'FAIL break-even', 'be=' + be.toFixed(2), 'profit=' + profitAtBE.toExponential(2));
if (!ok) failed++;

console.log(failed === 0 ? '\nALL CHECKS PASSED' : '\n' + failed + ' CHECK(S) FAILED');
process.exit(failed === 0 ? 0 : 1);
