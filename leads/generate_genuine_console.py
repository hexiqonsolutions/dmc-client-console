#!/usr/bin/env python3
"""Generate a simple outreach console from genuine_nm_100.json"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / "genuine_nm_100.json").read_text(encoding="utf-8"))
OUT = ROOT / "Genuine_NM_Console.html"

rows_js = json.dumps(DATA, ensure_ascii=False)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Genuine NM Clients — Outreach Console</title>
<style>
:root {{
  --bg:#0f1410; --panel:#182018; --line:#2a3a2c; --text:#e8efe6;
  --muted:#9bb09a; --accent:#7cb87a; --warn:#c9a227;
}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:Segoe UI,system-ui,sans-serif;background:var(--bg);color:var(--text)}}
header{{padding:16px 20px;border-bottom:1px solid var(--line);display:flex;gap:12px;flex-wrap:wrap;align-items:center}}
header h1{{margin:0;font-size:18px}}
.stats{{color:var(--muted);font-size:13px}}
.layout{{display:grid;grid-template-columns:340px 1fr;min-height:calc(100vh - 64px)}}
@media(max-width:900px){{.layout{{grid-template-columns:1fr}}}}
aside{{border-right:1px solid var(--line);overflow:auto;max-height:calc(100vh - 64px)}}
main{{padding:20px;overflow:auto}}
input,select,textarea{{width:100%;background:#101610;border:1px solid var(--line);color:var(--text);border-radius:8px;padding:10px;margin:6px 0 12px}}
.card{{padding:12px 14px;border-bottom:1px solid var(--line);cursor:pointer}}
.card:hover,.card.active{{background:var(--panel)}}
.card b{{display:block;font-size:14px}}
.card span{{color:var(--muted);font-size:12px}}
.badge{{display:inline-block;background:#243324;color:var(--accent);padding:2px 8px;border-radius:999px;font-size:11px;margin-top:6px}}
.actions{{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}}
a.btn,button.btn{{background:var(--accent);color:#0b120c;border:0;border-radius:8px;padding:10px 14px;font-weight:600;text-decoration:none;cursor:pointer}}
a.btn.secondary,button.btn.secondary{{background:#2a3a2c;color:var(--text)}}
.issue{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px;margin:12px 0;color:#d7e4d5;line-height:1.45}}
label{{font-size:12px;color:var(--muted)}}
</style>
</head>
<body>
<header>
  <h1>Genuine NM Clients</h1>
  <div class="stats" id="stats"></div>
</header>
<div class="layout">
  <aside>
    <div style="padding:12px">
      <input id="q" placeholder="Search company / owner / locality"/>
      <select id="industry"><option value="">All industries</option></select>
      <label><input type="checkbox" id="ownerOnly"/> Owner name only</label>
    </div>
    <div id="list"></div>
  </aside>
  <main id="detail">
    <p style="color:var(--muted)">Select a client from the left.</p>
  </main>
</div>
<script>
const ROWS = {rows_js};
const listEl = document.getElementById('list');
const detailEl = document.getElementById('detail');
const qEl = document.getElementById('q');
const indEl = document.getElementById('industry');
const ownerOnlyEl = document.getElementById('ownerOnly');
let activeId = null;

const industries = [...new Set(ROWS.map(r => r.industry).filter(Boolean))].sort();
industries.forEach(i => {{
  const o = document.createElement('option'); o.value = i; o.textContent = i; indEl.appendChild(o);
}});

function filtered() {{
  const q = qEl.value.trim().toLowerCase();
  const ind = indEl.value;
  return ROWS.filter(r => {{
    if (ownerOnlyEl.checked && !(r.owner||'').trim()) return false;
    if (ind && r.industry !== ind) return false;
    if (!q) return true;
    return [r.company,r.owner,r.locality,r.phone,r.email].join(' ').toLowerCase().includes(q);
  }});
}}

function renderList() {{
  const rows = filtered();
  document.getElementById('stats').textContent =
    `${{rows.length}} shown / ${{ROWS.length}} total · ${{ROWS.filter(r=>r.owner).length}} with owner · ${{ROWS.filter(r=>r.email&&r.email.includes('@')).length}} with email`;
  listEl.innerHTML = rows.map(r => `
    <div class="card ${{r.id===activeId?'active':''}}" data-id="${{r.id}}">
      <b>${{r.company}}</b>
      <span>${{r.owner||'Owner not listed'}} · ${{r.phone}}</span>
      <div class="badge">${{r.industry||'Business'}} · score ${{r.score}}</div>
    </div>`).join('');
  [...listEl.querySelectorAll('.card')].forEach(el => el.onclick = () => show(+el.dataset.id));
}}

function show(id) {{
  activeId = id;
  const r = ROWS.find(x => x.id === id);
  if (!r) return;
  renderList();
  detailEl.innerHTML = `
    <h2 style="margin:0 0 6px">${{r.company}}</h2>
    <div style="color:var(--muted);margin-bottom:10px">${{r.owner||'Owner not publicly listed'}} · ${{r.locality}} · ${{r.industry}}</div>
    <div><b>Phone:</b> ${{r.phone}} &nbsp; <b>Email:</b> ${{r.email||'—'}}</div>
    <div style="margin-top:6px"><b>Website:</b> <a style="color:var(--accent)" href="${{r.website}}" target="_blank" rel="noopener">${{r.website}}</a></div>
    <div class="issue"><b>Website issues (specific):</b><br>${{r.website_issues}}</div>
    <div class="issue"><b>Why they'll buy:</b><br>${{r.why_buy||''}}</div>
    <label>WhatsApp draft</label>
    <textarea id="wa" rows="8">${{r.whatsapp_msg||''}}</textarea>
    <label>Email subject</label>
    <input id="subj" value="${{(r.subject||'').replaceAll('"','&quot;')}}"/>
    <label>Email body</label>
    <textarea id="em" rows="10">${{r.email_body||''}}</textarea>
    <div class="actions">
      <a class="btn" id="waBtn" target="_blank" rel="noopener">Open WhatsApp</a>
      <a class="btn secondary" id="mailBtn">Open Email</a>
      <a class="btn secondary" href="${{r.website}}" target="_blank" rel="noopener">Open Website</a>
    </div>`;
  const sync = () => {{
    const wa = document.getElementById('wa').value;
    const subj = document.getElementById('subj').value;
    const em = document.getElementById('em').value;
    const digits = r.phone_digits || ('91' + (r.phone||'').replace(/\\D/g,'').slice(-10));
    document.getElementById('waBtn').href = `https://wa.me/${{digits}}?text=${{encodeURIComponent(wa)}}`;
    if (r.email && r.email.includes('@')) {{
      document.getElementById('mailBtn').href = `mailto:${{r.email}}?subject=${{encodeURIComponent(subj)}}&body=${{encodeURIComponent(em)}}`;
    }} else {{
      document.getElementById('mailBtn').removeAttribute('href');
      document.getElementById('mailBtn').onclick = () => alert('No email on file — use WhatsApp');
    }}
  }};
  ['wa','subj','em'].forEach(id => document.getElementById(id).oninput = sync);
  sync();
}}

qEl.oninput = renderList;
indEl.onchange = renderList;
ownerOnlyEl.onchange = renderList;
renderList();
if (ROWS[0]) show(ROWS[0].id);
</script>
</body>
</html>
"""

OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT.name} with {len(DATA)} leads")
print(f"Owners: {sum(1 for x in DATA if x.get('owner'))}")
print(f"Emails: {sum(1 for x in DATA if x.get('email') and '@' in x['email'])}")
