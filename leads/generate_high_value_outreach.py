#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build High-Value MMR client list + BuildView-style one-click outreach console."""

from __future__ import annotations

import json
import re
import urllib.parse
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(r"C:\Users\FPIN\Desktop\dm os\leads")
SEED = ROOT / "_seed_from_existing.json"
EXTRA = ROOT / "verified_extra_mmr.json"
JSON_OUT = ROOT / "high_value_prospects.json"
XLSX_OUT = ROOT / "High_Value_MMR_Clients.xlsx"
HTML_OUT = ROOT / "DMC_Client_Console.html"

SIGN = (
    "Regards,\n"
    "Vaibhav Gurav\n"
    "DMC Creatives Studio\n"
    "hello@dmcstudio.in\n"
    "www.dmcstudio.in\n"
    "+91 83693 61785"
)

INDUSTRY_ANGLE = {
    "Healthcare": "patients compare clinics online before they call — a clear website and booking path wins the enquiry",
    "Hotel / F&B": "guests and corporates book the hotel that looks trustworthy and easy on mobile",
    "Manufacturing": "B2B buyers shortlist suppliers from Google and catalogue sites before they raise an RFQ",
    "Education": "parents and students decide admissions from your website long before they walk in",
    "Automotive": "test-drive and service bookings now start online — weak dealer sites lose leads to competitors",
    "Real Estate / Design": "homebuyers and project clients judge your brand from the first project page they open",
    "Fitness": "memberships convert when the studio looks current and booking is one tap away",
    "Services": "serious clients still Google you — a weak site quietly costs you deals",
    "Business": "buyers judge readiness from your website before they ever call",
}


def extract_emails(raw: str) -> list[str]:
    if not raw:
        return []
    low = raw.lower()
    if "not found" in low or "gated" in low or "form only" in low:
        return []
    found = re.findall(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}", raw)
    out = []
    for e in found:
        el = e.lower()
        if "…" in e or e.endswith("@"):
            continue
        if re.search(r"@(g|ymail|yahoo|rediffmail|hotmail|gmail|vsnl)\.?$", el):
            # allow full gmail/yahoo etc — only skip truncated
            pass
        if e not in out:
            out.append(e)
    return out


def extract_mobiles(raw: str) -> list[str]:
    if not raw:
        return []
    low = raw.lower()
    if "not found" in low or "gated" in low or "show number" in low:
        return []
    compact = re.sub(r"[^\d+]", "", raw)
    out: list[str] = []
    for m in re.finditer(r"(?:91)?([6-9]\d{9})", compact):
        num = "91" + m.group(1)
        if num not in out:
            out.append(num)
    return out


def has_any_phone(raw: str) -> bool:
    if not raw:
        return False
    low = raw.lower()
    if "not found" in low or "gated" in low or "show number" in low:
        return False
    digits = re.sub(r"\D", "", raw)
    return bool(
        re.search(r"[6-9]\d{9}", digits)
        or re.search(r"0\d{9,11}", digits)
        or len(digits) >= 10
    )


def display_phone(e164: str) -> str:
    if e164.startswith("91") and len(e164) == 12:
        return "+91 " + e164[2:7] + " " + e164[7:]
    return e164


def first_name(dm: str) -> str:
    if not dm:
        return ""
    dm = re.sub(r"\([^)]*\)", "", dm).strip()
    parts = dm.replace(",", " ").replace("/", " ").split()
    skip = {"dr", "dr.", "mr", "mr.", "mrs", "mrs.", "ms", "ms.", "and", "team"}
    for p in parts:
        if p.lower().rstrip(".") in skip:
            continue
        if p and p[0].isalpha() and len(p) > 1:
            return p
    return ""


def greeting(dm: str) -> str:
    fn = first_name(dm)
    return f"Hi {fn}," if fn else "Hello,"


def subject_line(company: str, industry: str, wrong: str) -> str:
    short = company.split("(")[0].strip()
    w = (wrong or "").lower()
    if "no website" in w or "directory" in w or "indiamart" in w or "justdial" in w:
        return f"{short}: buyers search Google before they call"
    if "http" in w and "https" not in w:
        return f"{short} is still on HTTP — that hurts trust"
    if industry == "Healthcare":
        return f"{short}: patients shortlist clinics online first"
    if industry == "Hotel / F&B":
        return f"{short}: your website vs today's direct bookings"
    if industry == "Manufacturing":
        return f"{short}: RFQ buyers want a real catalogue site"
    if industry == "Education":
        return f"{short}: admissions start on your website"
    if industry == "Automotive":
        return f"{short}: test-drive leads are leaking online"
    if industry == "Real Estate / Design":
        return f"{short}: project pages that convert enquiries"
    return f"{short}'s website still looks stuck in the past"


def email_body(r: dict) -> str:
    company = r["company"]
    industry = r["industry"]
    locality = r["locality"]
    wrong = r["wrong"]
    offer = r["offer"]
    g = greeting(r.get("owner_or_dm") or "")
    angle = INDUSTRY_ANGLE.get(industry, INDUSTRY_ANGLE["Business"])
    area = locality or "Mumbai / Navi Mumbai / Thane"
    open_line = (
        f"While reviewing {industry.lower()} businesses in {area}, I came across {company}."
    )
    if "no website" in wrong.lower() or "directory" in wrong.lower() or "indiamart" in wrong.lower():
        problem = f"{company} still lacks a strong owned website buyers can trust."
    else:
        problem = (
            f"I reviewed {company}'s current digital presence — it works, "
            "but it no longer feels current or conversion-ready for today's market."
        )
    body = (
        f"{g}\n\n"
        f"{open_line}\n\n"
        f"{problem}\n\n"
        f"In this category, {angle}.\n\n"
        f"At DMC Creatives Studio we help MMR businesses with {offer.lower()}. "
        "Happy to share a free one-page concept for your brand this week — no obligation.\n\n"
        f"{SIGN}"
    )
    return body


def whatsapp_msg(r: dict) -> str:
    company = r["company"]
    g = greeting(r.get("owner_or_dm") or "")
    offer = r["offer"]
    return (
        f"{g}\n\n"
        f"I'm Vaibhav from DMC Creatives Studio. I was reviewing businesses in "
        f"{r.get('locality') or 'Mumbai / Navi Mumbai / Thane'} and noticed {company}'s "
        "website looks outdated for today's market.\n\n"
        f"We can help with {offer.lower()}. If useful, I can share a quick redesign concept — no obligation.\n\n"
        "Vaibhav Gurav\n"
        "DMC Creatives Studio\n"
        "hello@dmcstudio.in\n"
        "www.dmcstudio.in\n"
        "+91 83693 61785"
    )


def normalize_row(raw: dict) -> dict | None:
    company = (raw.get("company") or "").strip()
    if not company:
        return None
    email_raw = raw.get("email") or ""
    phone_raw = raw.get("phone") or ""
    emails = extract_emails(email_raw)
    mobiles = extract_mobiles(phone_raw)
    if not emails and not has_any_phone(phone_raw):
        return None
    priority = raw.get("priority") or "Medium"
    if priority not in {"High", "Medium", "Low"}:
        if "P1" in str(priority) or "P2" in str(priority) or "Hot" in str(priority):
            priority = "High"
        else:
            priority = "Medium"
    industry = (raw.get("industry") or "Business").strip()
    return {
        "company": company,
        "owner_or_dm": (raw.get("owner_or_dm") or raw.get("owner") or "").strip(),
        "designation": (raw.get("designation") or "").strip(),
        "email": emails[0] if emails else "",
        "emails": emails,
        "phone": phone_raw.strip(),
        "phones": mobiles,
        "website": (raw.get("website") or "").strip(),
        "wrong": (raw.get("wrong") or "").strip(),
        "industry": industry,
        "locality": (raw.get("locality") or "").strip(),
        "priority": priority,
        "offer": (raw.get("offer") or "Website redesign + lead capture").strip(),
        "value_note": (raw.get("value_note") or "").strip(),
        "source": (raw.get("source") or "").strip(),
    }


def load_all() -> list[dict]:
    rows: list[dict] = []
    seen = set()
    for path in (SEED, EXTRA):
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for raw in data:
            n = normalize_row(raw)
            if not n:
                continue
            key = n["company"].lower().strip()
            if key in seen:
                # Prefer row with email if duplicate
                existing = next(x for x in rows if x["company"].lower().strip() == key)
                if not existing["email"] and n["email"]:
                    rows.remove(existing)
                    rows.append(n)
                continue
            seen.add(key)
            rows.append(n)
    # Sort High first, then company
    rows.sort(key=lambda r: (0 if r["priority"] == "High" else 1, r["company"].lower()))
    return rows


def enrich(rows: list[dict]) -> list[dict]:
    for r in rows:
        r["subject"] = subject_line(r["company"], r["industry"], r["wrong"])
        r["email_body"] = email_body(r)
        r["whatsapp_msg"] = whatsapp_msg(r)
        r["wa_number"] = r["phones"][0] if r["phones"] else ""
        r["primary_phone_display"] = (
            display_phone(r["wa_number"]) if r["wa_number"] else (r["phone"] if has_any_phone(r["phone"]) else "")
        )
        if r["email"]:
            r["mailto"] = (
                "mailto:"
                + urllib.parse.quote(r["email"], safe="@.+_-")
                + "?"
                + urllib.parse.urlencode(
                    {"subject": r["subject"], "body": r["email_body"]},
                    quote_via=urllib.parse.quote,
                )
            )
        else:
            r["mailto"] = ""
        if r["wa_number"]:
            r["wa_link"] = (
                "https://wa.me/"
                + r["wa_number"]
                + "?text="
                + urllib.parse.quote(r["whatsapp_msg"])
            )
        else:
            r["wa_link"] = ""
    return rows


def write_excel(rows: list[dict]) -> Path:
    side = Side(style="thin", color="D0D0D0")
    border = Border(left=side, right=side, top=side, bottom=side)
    header_fill = PatternFill("solid", fgColor="0F172A")
    header_font = Font(bold=True, color="FFFFFF")
    prio_fill = {
        "High": PatternFill("solid", fgColor="C6EFCE"),
        "Medium": PatternFill("solid", fgColor="FFEDD5"),
        "Low": PatternFill("solid", fgColor="E0E7FF"),
    }
    wb = Workbook()
    ws = wb.active
    ws.title = "Contactable Clients"
    headers = [
        "Priority",
        "Company",
        "Industry",
        "Decision Maker",
        "Designation",
        "Email",
        "Phone / WhatsApp",
        "Website",
        "Locality",
        "What's Wrong",
        "Offer",
        "Value Note",
        "Email Subject",
        "Personalized Email",
        "Personalized WhatsApp",
        "SEND EMAIL",
        "SEND WHATSAPP",
        "Source",
    ]
    for c, h in enumerate(headers, 1):
        cell = ws.cell(1, c, h)
        cell.fill = header_fill
        cell.font = header_font
        cell.border = border
        cell.alignment = Alignment(wrap_text=True, vertical="center")

    for i, r in enumerate(rows, 2):
        vals = [
            r["priority"],
            r["company"],
            r["industry"],
            r["owner_or_dm"],
            r["designation"],
            r["email"],
            r["primary_phone_display"] or r["phone"],
            r["website"],
            r["locality"],
            r["wrong"],
            r["offer"],
            r["value_note"],
            r["subject"],
            r["email_body"],
            r["whatsapp_msg"],
            "CLICK TO EMAIL" if r["mailto"] else "",
            "CLICK WHATSAPP" if r["wa_link"] else "",
            r["source"],
        ]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(i, c, v or "")
            cell.border = border
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            if c == 1 and v in prio_fill:
                cell.fill = prio_fill[v]
            if c == 6 and v and "@" in str(v):
                cell.hyperlink = f"mailto:{v}"
                cell.font = Font(color="0563C1", underline="single")
            if c == 16 and r["mailto"]:
                cell.hyperlink = r["mailto"]
                cell.font = Font(color="0563C1", underline="single")
            if c == 17 and r["wa_link"]:
                cell.hyperlink = r["wa_link"]
                cell.font = Font(color="128C7E", underline="single")
        ws.row_dimensions[i].height = 72

    widths = [10, 26, 16, 20, 18, 28, 18, 28, 20, 36, 26, 22, 34, 42, 36, 14, 14, 18]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:R{len(rows)+1}"

    ws2 = wb.create_sheet("High Priority")
    h2 = ["Company", "To", "Phone", "Subject", "Email Body", "WhatsApp", "CLICK EMAIL", "CLICK WHATSAPP"]
    for c, h in enumerate(h2, 1):
        cell = ws2.cell(1, c, h)
        cell.fill = header_fill
        cell.font = header_font
    ri = 2
    for r in rows:
        if r["priority"] != "High":
            continue
        vals = [
            r["company"],
            r["email"] or "(use WhatsApp)",
            r["primary_phone_display"] or r["phone"],
            r["subject"],
            r["email_body"],
            r["whatsapp_msg"] if r["wa_link"] else "(no WhatsApp mobile)",
            "CLICK TO EMAIL" if r["mailto"] else "No email",
            "CLICK WHATSAPP" if r["wa_link"] else "No WA",
        ]
        for c, v in enumerate(vals, 1):
            cell = ws2.cell(ri, c, v)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = border
        if r["mailto"]:
            ws2.cell(ri, 7).hyperlink = r["mailto"]
            ws2.cell(ri, 7).font = Font(color="0563C1", underline="single")
        if r["wa_link"]:
            ws2.cell(ri, 8).hyperlink = r["wa_link"]
            ws2.cell(ri, 8).font = Font(color="128C7E", underline="single")
        ws2.row_dimensions[ri].height = 100
        ri += 1
    for i, w in enumerate([22, 28, 16, 34, 48, 36, 14, 14], 1):
        ws2.column_dimensions[get_column_letter(i)].width = w

    wb.save(XLSX_OUT)
    return XLSX_OUT


def write_html(rows: list[dict]) -> Path:
    contacts = [
        {
            "priority": r["priority"],
            "company": r["company"],
            "industry": r["industry"],
            "dm": r["owner_or_dm"],
            "des": r["designation"],
            "email": r["email"],
            "phone": r["primary_phone_display"] or r["phone"],
            "website": r["website"],
            "locality": r["locality"],
            "wrong": r["wrong"],
            "offer": r["offer"],
            "valueNote": r["value_note"],
            "subject": r["subject"],
            "emailBody": r["email_body"],
            "whatsappMsg": r["whatsapp_msg"],
            "mailto": r["mailto"],
            "waLink": r["wa_link"],
            "waNumber": r["wa_number"],
        }
        for r in rows
    ]
    contacts_js = json.dumps(contacts, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>DMC Client Console</title>
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@500;600;700&family=Fira+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
:root {{
  --color-primary: #2563EB;
  --color-on-primary: #FFFFFF;
  --color-secondary: #3B82F6;
  --color-accent: #059669;
  --color-background: #F8FAFC;
  --color-foreground: #0F172A;
  --color-muted: #F1F5FD;
  --color-border: #E4ECFC;
  --color-destructive: #DC2626;
  --color-ring: #2563EB;
  --text-muted: #64748B;
  --surface: #FFFFFF;
  --wa: #128C7E;
  --high: #059669;
  --med: #D97706;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 24px;
  --radius: 10px;
  --font: "Fira Sans", system-ui, sans-serif;
  --mono: "Fira Code", ui-monospace, monospace;
  --shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
}}
* {{ box-sizing: border-box; }}
html, body {{ height: 100%; }}
body {{
  margin: 0;
  font-family: var(--font);
  background: var(--color-background);
  color: var(--color-foreground);
  line-height: 1.45;
}}
button, a, input, select, textarea {{ font: inherit; }}
button, .btn, a.btn {{ cursor: pointer; transition: background-color 180ms ease, border-color 180ms ease, color 180ms ease; }}
button:focus-visible, a:focus-visible, input:focus-visible, select:focus-visible, textarea:focus-visible {{
  outline: 2px solid var(--color-ring);
  outline-offset: 2px;
}}
@media (prefers-reduced-motion: reduce) {{
  * {{ transition: none !important; animation: none !important; }}
}}
header {{
  padding: var(--space-4) var(--space-5) var(--space-3);
  background: var(--surface);
  border-bottom: 1px solid var(--color-border);
}}
header h1 {{
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}}
header p {{
  margin: 4px 0 0;
  color: var(--text-muted);
  font-size: 0.88rem;
  max-width: 820px;
}}
.toolbar {{
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  align-items: center;
  padding: var(--space-3) var(--space-5);
  background: rgba(248,250,252,0.96);
  border-bottom: 1px solid var(--color-border);
  position: sticky;
  top: 0;
  z-index: 20;
  backdrop-filter: blur(8px);
}}
input, select {{
  background: var(--surface);
  color: var(--color-foreground);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 0.88rem;
  min-height: 40px;
}}
input:hover, select:hover {{ border-color: #c7d7f8; }}
input[type=search] {{ min-width: 220px; flex: 1; }}
.stats {{ display: flex; gap: 8px; flex-wrap: wrap; margin-left: auto; }}
.chip {{
  font-size: 0.75rem;
  font-weight: 600;
  padding: 6px 10px;
  border-radius: 999px;
  background: var(--color-muted);
  color: var(--color-foreground);
  border: 1px solid var(--color-border);
  font-family: var(--mono);
}}
.layout {{
  display: grid;
  grid-template-columns: 340px 1fr;
  min-height: calc(100vh - 150px);
}}
@media (max-width: 900px) {{
  .layout {{ grid-template-columns: 1fr; }}
  .list {{ max-height: 38vh; }}
}}
.list {{
  border-right: 1px solid var(--color-border);
  overflow: auto;
  max-height: calc(100vh - 150px);
  background: var(--surface);
}}
.item {{
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
}}
.item:hover {{ background: #F8FAFF; }}
.item.active {{
  background: #EFF6FF;
  box-shadow: inset 3px 0 0 var(--color-primary);
}}
.item .co {{ font-weight: 600; font-size: 0.92rem; }}
.item .meta {{ color: var(--text-muted); font-size: 0.78rem; margin-top: 3px; }}
.prio {{
  display: inline-block;
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: .04em;
  padding: 2px 7px;
  border-radius: 4px;
  margin-right: 6px;
  text-transform: uppercase;
  font-family: var(--mono);
}}
.prio.High {{ background: #D1FAE5; color: #065F46; }}
.prio.Medium {{ background: #FFEDD5; color: #9A3412; }}
.prio.Low {{ background: #E0E7FF; color: #3730A3; }}
.detail {{
  padding: 20px 24px 48px;
  overflow: auto;
  max-height: calc(100vh - 150px);
}}
.empty {{
  color: var(--text-muted);
  padding: 48px 24px;
  text-align: center;
}}
.detail h2 {{ margin: 0 0 4px; font-size: 1.35rem; letter-spacing: -0.02em; }}
.sub {{ color: var(--text-muted); font-size: 0.88rem; margin-bottom: 14px; }}
.kv {{
  display: grid;
  grid-template-columns: 120px 1fr;
  gap: 6px 10px;
  font-size: 0.88rem;
  margin-bottom: 14px;
  padding: 12px 14px;
  background: var(--surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
}}
.kv span:nth-child(odd) {{ color: var(--text-muted); font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: .03em; }}
.kv a {{ color: var(--color-primary); }}
.actions {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0 10px; }}
.btn {{
  appearance: none;
  border: 1px solid transparent;
  border-radius: 8px;
  min-height: 44px;
  padding: 0 14px;
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  background: var(--color-muted);
}}
.btn svg {{ width: 16px; height: 16px; flex-shrink: 0; }}
.btn-email {{ background: var(--color-accent); }}
.btn-email:hover {{ background: #047857; }}
.btn-wa {{ background: var(--wa); }}
.btn-wa:hover {{ background: #0f766e; }}
.btn-copy {{ background: var(--color-primary); }}
.btn-copy:hover {{ background: #1d4ed8; }}
.btn-ghost {{ background: #fff; color: var(--color-foreground); border-color: var(--color-border); }}
.btn-ghost:hover {{ background: var(--color-muted); }}
.btn:disabled {{ opacity: .45; cursor: not-allowed; }}
.hint {{ font-size: 0.78rem; color: var(--text-muted); margin: 0 0 14px; line-height: 1.4; }}
.grid2 {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}}
@media (max-width: 1100px) {{ .grid2 {{ grid-template-columns: 1fr; }} }}
.card {{
  background: var(--surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 14px;
  box-shadow: var(--shadow);
}}
.card h3 {{
  margin: 0 0 10px;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: .06em;
  color: var(--text-muted);
}}
.field {{ margin-bottom: 10px; }}
.field label {{
  display: block;
  font-size: 0.72rem;
  font-weight: 600;
  color: var(--text-muted);
  margin-bottom: 4px;
  text-transform: uppercase;
  letter-spacing: .04em;
}}
.field input, .field textarea {{
  width: 100%;
  background: #F8FAFF;
  border: 1px solid var(--color-border);
  color: var(--color-foreground);
  border-radius: 8px;
  padding: 10px;
  font-size: 0.88rem;
  resize: vertical;
}}
textarea {{ min-height: 260px; line-height: 1.45; font-family: var(--font); }}
.toast {{
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: var(--color-accent);
  color: #fff;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  opacity: 0;
  pointer-events: none;
  transition: opacity .2s;
  z-index: 50;
}}
.toast.show {{ opacity: 1; }}
.item {{
  opacity: 0;
  transform: translateY(8px);
  animation: fadeUp 280ms ease forwards;
}}
@keyframes fadeUp {{
  to {{ opacity: 1; transform: translateY(0); }}
}}
</style>
</head>
<body>
<header>
  <h1>DMC Client Console</h1>
  <p>Mumbai + Navi Mumbai + Thane high-value clients with outdated websites. Personalized email & WhatsApp drafts. Signed as Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.</p>
</header>
<div class="toolbar">
  <input type="search" id="q" placeholder="Search company, person, industry, locality…" />
  <select id="priority">
    <option value="All">All priorities</option>
    <option value="High">High</option>
    <option value="Medium">Medium</option>
  </select>
  <select id="industry"><option value="All">All industries</option></select>
  <select id="contact">
    <option value="All">Any contact</option>
    <option value="email">Has email</option>
    <option value="wa">Has WhatsApp</option>
    <option value="both">Email + WhatsApp</option>
  </select>
  <div class="stats">
    <span class="chip" id="countChip">0 shown</span>
    <span class="chip" id="highChip">0 High</span>
    <span class="chip" id="emailChip">0 email</span>
    <span class="chip" id="waChip">0 WhatsApp</span>
  </div>
</div>
<div class="layout">
  <div class="list" id="list"></div>
  <div class="detail" id="detail"><div class="empty">Select a company to view and send their personalized message.</div></div>
</div>
<div class="toast" id="toast">Copied</div>
<script>
const CONTACTS = {contacts_js};

const listEl = document.getElementById('list');
const detailEl = document.getElementById('detail');
const qEl = document.getElementById('q');
const pEl = document.getElementById('priority');
const iEl = document.getElementById('industry');
const cEl = document.getElementById('contact');
const toast = document.getElementById('toast');
let selected = null;

[...new Set(CONTACTS.map(c => c.industry).filter(Boolean))].sort().forEach(c => {{
  const o = document.createElement('option');
  o.value = c; o.textContent = c; iEl.appendChild(o);
}});

function toastMsg(msg) {{
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 1800);
}}

function filtered() {{
  const q = qEl.value.trim().toLowerCase();
  return CONTACTS.filter(c => {{
    if (pEl.value !== 'All' && c.priority !== pEl.value) return false;
    if (iEl.value !== 'All' && c.industry !== iEl.value) return false;
    if (cEl.value === 'email' && !c.email) return false;
    if (cEl.value === 'wa' && !c.waNumber) return false;
    if (cEl.value === 'both' && !(c.email && c.waNumber)) return false;
    if (!q) return true;
    return `${{c.company}} ${{c.dm}} ${{c.des}} ${{c.industry}} ${{c.email}} ${{c.locality}} ${{c.offer}}`.toLowerCase().includes(q);
  }});
}}

function updateStats(rows) {{
  document.getElementById('countChip').textContent = rows.length + ' shown';
  document.getElementById('highChip').textContent = rows.filter(r => r.priority === 'High').length + ' High';
  document.getElementById('emailChip').textContent = rows.filter(r => r.email).length + ' email';
  document.getElementById('waChip').textContent = rows.filter(r => r.waNumber).length + ' WhatsApp';
}}

function renderList() {{
  const rows = filtered();
  updateStats(rows);
  listEl.innerHTML = rows.map((c, idx) => `
    <div class="item ${{selected && selected.company === c.company ? 'active' : ''}}" data-company="${{c.company.replace(/"/g,'&quot;')}}" style="animation-delay:${{Math.min(idx, 12) * 30}}ms">
      <div class="co"><span class="prio ${{c.priority}}">${{c.priority}}</span>${{esc(c.company)}}</div>
      <div class="meta">${{esc(c.industry)}} · ${{esc(c.dm) || 'No named contact'}} · ${{esc(c.locality)}}</div>
    </div>
  `).join('');
  listEl.querySelectorAll('.item').forEach(el => {{
    el.addEventListener('click', () => {{
      selected = CONTACTS.find(x => x.company === el.dataset.company);
      renderList();
      renderDetail();
    }});
  }});
}}

function esc(s) {{
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

function iconMail() {{
  return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 6h16v12H4z"/><path d="m4 7 8 6 8-6"/></svg>';
}}
function iconWa() {{
  return '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.7 14.9L2 22l5.3-1.4A10 10 0 1 0 12 2zm0 18a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 20zm4.4-5.9c-.2-.1-1.4-.7-1.6-.8s-.4-.1-.5.1-.6.8-.8 1-.3.2-.5.1a6.5 6.5 0 0 1-3.2-2.8c-.2-.4.2-.4.6-1.3.1-.1 0-.3 0-.4s-.5-1.2-.7-1.6-.4-.4-.5-.4h-.4c-.2 0-.4.1-.6.3a2 2 0 0 0-.6 1.5 3.5 3.5 0 0 0 .7 1.8 8 8 0 0 0 3.1 2.9 10.5 10.5 0 0 0 2.3.9 2.2 2.2 0 0 0 1.6.1 2.7 2.7 0 0 0 1.1-1c.1-.3.1-.5.1-.5s-.1-.1-.3-.2z"/></svg>';
}}

function renderDetail() {{
  if (!selected) {{
    detailEl.innerHTML = '<div class="empty">Select a company to view and send their personalized message.</div>';
    return;
  }}
  const c = selected;
  detailEl.innerHTML = `
    <h2>${{esc(c.company)}}</h2>
    <div class="sub"><span class="prio ${{c.priority}}">${{c.priority}}</span> ${{esc(c.industry)}} · ${{esc(c.locality)}}</div>
    <div class="kv">
      <span>Decision maker</span><span>${{esc(c.dm) || '—'}} ${{c.des ? '· ' + esc(c.des) : ''}}</span>
      <span>Email</span><span>${{esc(c.email) || 'No public email — use WhatsApp'}}</span>
      <span>Phone</span><span style="font-family:var(--mono)">${{esc(c.phone) || '—'}}</span>
      <span>Website</span><span>${{c.website && c.website.startsWith('http') ? `<a href="${{esc(c.website)}}" target="_blank" rel="noopener">${{esc(c.website)}}</a>` : esc(c.website) || '—'}}</span>
      <span>What's wrong</span><span>${{esc(c.wrong)}}</span>
      <span>Offer</span><span>${{esc(c.offer)}}</span>
    </div>
    <div class="actions">
      ${{c.mailto ? `<a class="btn btn-email" id="sendEmail" href="${{esc(c.mailto)}}">${{iconMail()}} Send Email (1-click)</a>` : `<button class="btn btn-email" disabled>No email on file</button>`}}
      ${{c.waLink ? `<a class="btn btn-wa" id="sendWa" href="${{esc(c.waLink)}}" target="_blank" rel="noopener">${{iconWa()}} WhatsApp (1-click)</a>` : `<button class="btn btn-wa" disabled>No WhatsApp number</button>`}}
      <button class="btn btn-copy" id="copyEmail">Copy Email</button>
      <button class="btn btn-copy" id="copyWa">Copy WhatsApp</button>
      <button class="btn btn-ghost" id="copyAll">Copy Subject + Email</button>
    </div>
    <p class="hint">Email opens Outlook/Gmail with draft filled. WhatsApp opens wa.me with the message ready (mobile numbers only). Edit drafts below — links rebuild live.</p>
    <div class="grid2">
      <div class="card">
        <h3>Email draft</h3>
        <div class="field"><label>Subject</label><input id="subj" value="${{esc(c.subject)}}" /></div>
        <div class="field"><label>Body (editable)</label><textarea id="body">${{esc(c.emailBody)}}</textarea></div>
      </div>
      <div class="card">
        <h3>WhatsApp message</h3>
        <div class="field"><label>Message (editable)</label><textarea id="wamsg">${{esc(c.whatsappMsg)}}</textarea></div>
        <p class="hint">${{c.waNumber ? 'Will send to +' + esc(c.waNumber) : 'No usable mobile — copy and send manually if you have another number.'}}</p>
      </div>
    </div>
  `;

  const subj = document.getElementById('subj');
  const body = document.getElementById('body');
  const wamsg = document.getElementById('wamsg');
  const send = document.getElementById('sendEmail');
  const sendWa = document.getElementById('sendWa');

  function rebuildMailto() {{
    if (!send || !c.email) return;
    send.href = 'mailto:' + encodeURIComponent(c.email).replace(/%40/g,'@')
      + '?subject=' + encodeURIComponent(subj.value)
      + '&body=' + encodeURIComponent(body.value);
  }}
  function rebuildWa() {{
    if (!sendWa || !c.waNumber) return;
    sendWa.href = 'https://wa.me/' + c.waNumber + '?text=' + encodeURIComponent(wamsg.value);
  }}
  subj.addEventListener('input', rebuildMailto);
  body.addEventListener('input', rebuildMailto);
  wamsg.addEventListener('input', rebuildWa);

  document.getElementById('copyEmail').onclick = () => {{
    navigator.clipboard.writeText(body.value); toastMsg('Email body copied');
  }};
  document.getElementById('copyWa').onclick = () => {{
    navigator.clipboard.writeText(wamsg.value); toastMsg('WhatsApp message copied');
  }};
  document.getElementById('copyAll').onclick = () => {{
    navigator.clipboard.writeText('Subject: ' + subj.value + '\\n\\n' + body.value);
    toastMsg('Subject + email copied');
  }};
}}

qEl.addEventListener('input', renderList);
pEl.addEventListener('change', renderList);
iEl.addEventListener('change', renderList);
cEl.addEventListener('change', renderList);
renderList();
const firstHigh = CONTACTS.find(c => c.priority === 'High') || CONTACTS[0];
if (firstHigh) {{ selected = firstHigh; renderList(); renderDetail(); }}
</script>
</body>
</html>
"""
    HTML_OUT.write_text(html, encoding="utf-8")
    return HTML_OUT


def main() -> None:
    rows = enrich(load_all())
    JSON_OUT.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    write_excel(rows)
    write_html(rows)
    with_email = sum(1 for r in rows if r["email"])
    with_wa = sum(1 for r in rows if r["wa_number"])
    high = sum(1 for r in rows if r["priority"] == "High")
    print(f"Contactable: {len(rows)}")
    print(f"High: {high} | Email: {with_email} | WhatsApp: {with_wa}")
    print(f"Wrote {JSON_OUT.name}")
    print(f"Wrote {XLSX_OUT.name}")
    print(f"Wrote {HTML_OUT.name}")
    assert len(rows) >= 100, f"Expected 100+ contactable, got {len(rows)}"


if __name__ == "__main__":
    main()
