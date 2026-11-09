#!/usr/bin/env python3
"""Build the blind rating page for the human check in docs/PLAN-v4.md.

Pairs each acme answer with the ref answer of the same case and run, redacts skill names,
puts them on random sides, and writes:
  OUT.html       the page (no arm labels anywhere in it)
  OUT.key.json   which side was which arm, kept locally to score the ratings afterwards

Usage:
  rating_page.py --acme ACME.json --ref REF.json --cases CASES --names skill_names.json \
      --prefix d-writing --out DIR/rating

Exit status: 0.
"""
from __future__ import annotations

import argparse
import html
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pairwise import body, load_arm, redactor  # noqa: E402

PAGE = """<title>Blind Writing Pairs</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: one reading column of pair cards; the two drafts sit side by side on wide screens */
:root {
  --bg: #f6f7f4; --surface: #ffffff; --fg: #1d2420; --muted: #5d6862; --line: #d9ded8;
  --accent: #2f6b4f; --accent-ink: #ffffff; --chosen: #e3efe7;
  --font-body: "Source Serif 4", Georgia, serif; --font-ui: "IBM Plex Sans", system-ui, sans-serif;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #141816; --surface: #1c211e; --fg: #e4e9e5; --muted: #9aa59f; --line: #333b36;
  --accent: #7cc49d; --accent-ink: #0e1511; --chosen: #22352a; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #141816; --surface: #1c211e; --fg: #e4e9e5; --muted: #9aa59f; --line: #333b36;
  --accent: #7cc49d; --accent-ink: #0e1511; --chosen: #22352a; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font-family: var(--font-ui); font-size: 15px; line-height: 1.5;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 24px 64px; }
main { max-width: 1120px; margin: 0 auto; display: grid; gap: 28px; }
header { display: grid; gap: 8px; max-width: 70ch; }
h1 { font-family: var(--font-body); font-size: 30px; font-weight: 600; margin: 0; text-wrap: balance; }
p { margin: 0; }
.muted { color: var(--muted); }
.progress { font-variant-numeric: tabular-nums; font-weight: 600; }
.status { font-size: 13px; color: var(--muted); }
article { background: var(--surface); border: 1px solid var(--line); border-radius: 6px; padding: 20px; display: grid; gap: 16px; }
.eyebrow { font-size: 12px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
details summary { cursor: pointer; font-weight: 600; }
details pre { white-space: pre-wrap; font-size: 13px; background: var(--bg); border: 1px solid var(--line); border-radius: 4px; padding: 12px; overflow-x: auto; margin: 8px 0 0; }
.drafts { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 760px) { .drafts { grid-template-columns: 1fr; } }
.draft { min-width: 0; border-top: 3px solid var(--line); padding-top: 10px; font-family: var(--font-body); font-size: 16px; }
.draft h3 { font-family: var(--font-ui); font-size: 13px; margin: 0 0 6px; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); }
.draft.picked { border-top-color: var(--accent); }
.draft pre, .draft code { font-size: 13px; white-space: pre-wrap; overflow-wrap: anywhere; }
.draft table { display: block; overflow-x: auto; border-collapse: collapse; }
.draft td, .draft th { border: 1px solid var(--line); padding: 4px 8px; }
.choices { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
button { font: inherit; font-weight: 600; padding: 8px 14px; border-radius: 4px; border: 1px solid var(--line); background: var(--surface); color: var(--fg); cursor: pointer; }
button:focus-visible, textarea:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
button[aria-pressed="true"] { background: var(--accent); color: var(--accent-ink); border-color: var(--accent); }
button:disabled { opacity: .5; cursor: not-allowed; }
textarea { font: inherit; width: 100%; box-sizing: border-box; min-height: 52px; padding: 8px; border: 1px solid var(--line); border-radius: 4px; background: var(--bg); color: var(--fg); }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<main>
  <header>
    <h1>Blind Writing Pairs</h1>
    <p>Each card shows one request and two drafts written for it. Pick the one you would rather send as written, or "About the same". The drafts come from two different setups, shuffled so you can't tell which is which. A note is optional.</p>
    <p><span class="progress" id="progress">0 of __N__ rated</span> <span class="status" id="status">Connecting to saved ratings…</span></p>
  </header>
  <div id="pairs" style="display:grid;gap:28px"></div>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.0.6/purify.min.js"></script>
<script>
const PAIRS = __PAIRS__;
const ratings = {};
let db = null;
const md = t => { try { return DOMPurify.sanitize(marked.parse(t)); } catch (e) { const d = document.createElement('div'); d.style.whiteSpace = 'pre-wrap'; d.textContent = t; return d.outerHTML; } };
function render() {
  const root = document.getElementById('pairs');
  root.textContent = '';
  PAIRS.forEach((p, i) => {
    const r = ratings[p.id] || {};
    const a = document.createElement('article');
    a.innerHTML = `<div class="eyebrow">Pair ${i + 1} of ${PAIRS.length}</div>
      <details><summary>The request</summary><pre></pre></details>
      <div class="drafts"><section class="draft ${r.choice === 'A' ? 'picked' : ''}"><h3>Draft A</h3><div class="body"></div></section>
      <section class="draft ${r.choice === 'B' ? 'picked' : ''}"><h3>Draft B</h3><div class="body"></div></section></div>
      <div class="choices" role="group" aria-label="Your choice for pair ${i + 1}"></div>
      <label class="muted" for="note-${p.id}">Note (optional)</label><textarea id="note-${p.id}"></textarea>`;
    a.querySelector('pre').textContent = p.request;
    const bodies = a.querySelectorAll('.body');
    bodies[0].innerHTML = md(p.a); bodies[1].innerHTML = md(p.b);
    const group = a.querySelector('.choices');
    [['A', 'Draft A reads better'], ['same', 'About the same'], ['B', 'Draft B reads better']].forEach(([v, label]) => {
      const b = document.createElement('button');
      b.textContent = label; b.setAttribute('aria-pressed', String(r.choice === v)); b.disabled = !db;
      b.addEventListener('click', () => save(p.id, { choice: v }));
      group.appendChild(b);
    });
    const note = a.querySelector('textarea');
    note.value = r.note || ''; note.disabled = !db;
    note.addEventListener('change', () => save(p.id, { note: note.value.slice(0, 2000) }));
    root.appendChild(a);
  });
  const done = PAIRS.filter(p => (ratings[p.id] || {}).choice).length;
  document.getElementById('progress').textContent = `${done} of ${PAIRS.length} rated`;
}
async function save(id, patch) {
  const next = Object.assign({}, ratings[id] || {}, patch, { at: new Date().toISOString() });
  ratings[id] = next; render();
  try { await db.doc('ratings/' + id).set(next); setStatus('Saved'); }
  catch (e) { setStatus('Could not save that choice. Check your connection and pick again.'); }
}
function setStatus(t) { document.getElementById('status').textContent = t; }
render();
(async () => {
  const timer = setTimeout(() => setStatus('Saved ratings did not load. Reload the page to try again.'), 10000);
  try {
    db = window.claude ? await window.claude.use('db') : null;
    if (!db) { clearTimeout(timer); setStatus('Open this page signed in to claude.ai to save ratings.'); render(); return; }
    db.collection('ratings').onSnapshot(snap => {
      clearTimeout(timer);
      (snap.docs || []).forEach(d => { ratings[d.id] = d.data ? d.data() : d; });
      setStatus('Choices save as you click.'); render();
    }, () => { clearTimeout(timer); setStatus('Saved ratings did not load. Reload the page to try again.'); });
  } catch (e) { clearTimeout(timer); setStatus('Saving is unavailable here.'); }
})();
</script>
"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--acme", type=Path, required=True)
    parser.add_argument("--ref", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--names", type=Path, required=True)
    parser.add_argument("--prefix", default="d-writing")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    acme, ref = load_arm(args.acme), load_arm(args.ref)
    redact = redactor(json.loads(args.names.read_text()))
    rng = random.Random(4)
    pairs, key = [], {}
    for case in sorted(c for c in acme if c.startswith(args.prefix)):
        request = body((args.cases / case / "prompt.md").read_text())
        request = request.split("\n", 1)[1].strip() if request.startswith("(Context") else request
        for run, (ra, rr) in enumerate(zip(acme[case], ref[case])):
            if not ra["answer"] or not rr["answer"]:
                continue
            pid = f"p{len(pairs) + 1:02d}"
            acme_left = rng.random() < 0.5
            a, b = (ra, rr) if acme_left else (rr, ra)
            pairs.append({"id": pid, "request": request, "a": redact(a["answer"]), "b": redact(b["answer"])})
            key[pid] = {"case": case, "run": run, "A": "acme" if acme_left else "ref", "B": "ref" if acme_left else "acme"}
    rng.shuffle(pairs)
    page = PAGE.replace("__N__", str(len(pairs))).replace("__PAIRS__", json.dumps(pairs).replace("</", "<\\/"))
    args.out.with_suffix(".html").write_text(page, encoding="utf-8")
    args.out.with_suffix(".key.json").write_text(json.dumps(key, indent=2))
    print(f"{len(pairs)} pairs -> {args.out.with_suffix('.html')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
