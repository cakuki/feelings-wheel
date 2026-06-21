// fit_check.js — the feedback loop that keeps every label inside its shape.
//
// Eyeballing a PNG is an open loop: you guess a font size, render, squint, repeat.
// This closes it. Load duygu-carki.html in a browser, run this function, and it
// reports — from the REAL rendered geometry — any label that crosses out of the
// ring (or circle) it belongs to. Drive font sizes in gen_wheel.py from `fails`,
// not from guesses.
//
// How to run:
//   • Browser DevTools console: paste the body and call fitCheck().
//   • Chrome DevTools MCP: evaluate_script with this function.
//
// Geometry must match gen_wheel.py:
const FIT = { CX: 350, CY: 350, R_CENTER: 90, R_CORE: 178, R_OUTER: 300, MARGIN: 2 };

function fitCheck() {
  const { CX, CY, R_CENTER, R_CORE, R_OUTER, MARGIN } = FIT;
  const out = [];
  for (const t of document.querySelectorAll('svg text')) {
    const x = parseFloat(t.getAttribute('x'));
    const y = parseFloat(t.getAttribute('y'));
    const bb = t.getBBox();
    const isRadial = !!t.getAttribute('transform'); // rotated labels run radially

    if (isRadial) {
      // Text lies ALONG the radius; its width is its radial extent.
      const dist = Math.hypot(x - CX, y - CY);
      const rmin = dist - bb.width / 2, rmax = dist + bb.width / 2;
      const [lo, hi] = dist < R_CORE ? [R_CENTER, R_CORE] : [R_CORE, R_OUTER];
      out.push({
        text: t.textContent, kind: dist < R_CORE ? 'core' : 'outer',
        fontSize: parseFloat(t.getAttribute('font-size')),
        innerGap: +(rmin - lo).toFixed(1),  // <0 => pokes into the inner shape
        outerGap: +(hi - rmax).toFixed(1),  // <0 => spills past the outer edge
        fits: rmin >= lo - MARGIN && rmax <= hi + MARGIN,
      });
    } else {
      // Center prompt: horizontal text; must fit the circle's chord at its y.
      const dy = Math.abs(y - CY);
      const halfChord = Math.sqrt(Math.max(0, R_CENTER * R_CENTER - dy * dy));
      const slack = +(halfChord - bb.width / 2).toFixed(1); // <0 => overflows
      out.push({
        text: t.textContent, kind: 'center',
        fontSize: parseFloat(t.getAttribute('font-size')),
        slack, fits: bb.width / 2 <= halfChord - MARGIN,
      });
    }
  }
  return { ok: out.every(o => o.fits), fails: out.filter(o => !o.fits), all: out };
}

if (typeof module !== 'undefined') module.exports = { fitCheck, FIT };
