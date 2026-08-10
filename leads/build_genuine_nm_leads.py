#!/usr/bin/env python3
"""
Build a quality-gated Navi Mumbai / MMR lead list.

Quality gates (strict):
- Must have a real 10-digit phone
- Must have website URL OR explicit no-website with Google-visible phone
- Must NOT reuse phones already in exclude list
- Must have individual website_issues (not generic template text)
- Prefer named owner

Usage:
  1. Drop researched batches into genuine_batches/*.json (arrays)
  2. python build_genuine_nm_leads.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from collections import Counter

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent
BATCH_DIR = ROOT / "genuine_batches"
OUT_JSON = ROOT / "genuine_nm_100.json"
OUT_XLSX = ROOT / "Genuine_NM_100_Clients.xlsx"
EXCLUDE_PHONES = set(json.loads((ROOT / "_exclude_phones.json").read_text(encoding="utf-8"))) if (ROOT / "_exclude_phones.json").exists() else set()
EXCLUDE_COMPANIES = set(json.loads((ROOT / "_exclude_companies.json").read_text(encoding="utf-8"))) if (ROOT / "_exclude_companies.json").exists() else set()

PHONE_RE = re.compile(r"(?:\+?91[\s\-]?)?([6-9]\d{9})")


def norm_phone(raw: str) -> str:
    digits = re.sub(r"\D", "", raw or "")
    if digits.startswith("91") and len(digits) >= 12:
        digits = digits[-10:]
    if len(digits) == 10 and digits[0] in "6789":
        return digits
    return ""


def display_phone(p: str) -> str:
    return f"+91 {p[:5]} {p[5:]}" if len(p) == 10 else p


def load_batches() -> list[dict]:
    rows: list[dict] = []
    if not BATCH_DIR.exists():
        return rows
    for path in sorted(BATCH_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            data = data.get("leads") or data.get("prospects") or []
        for row in data:
            row["_batch"] = path.name
            rows.append(row)
    return rows


GENERIC_ISSUES = {
    "outdated website",
    "needs website",
    "website needs improvement",
    "looks outdated",
}


def is_specific_issue(text: str) -> bool:
    t = (text or "").strip().lower()
    if len(t) < 40:
        return False
    if t in GENERIC_ISSUES:
        return False
    # Require at least one concrete signal
    signals = [
        "booking", "whatsapp", "mobile", "http", "gmail", "copyright",
        "template", "flash", "jquery", "wordpress", "elementor", "order",
        "menu", "enquiry", "contact", "broken", "lorem", "table", "frame",
        "no website", "zomato", "swiggy", "justdial", "indiamart", "practo",
        "ssl", "slow", "popup", "stock photo", "no price", "no cta",
    ]
    return any(s in t for s in signals)


def qualify(row: dict) -> tuple[bool, str]:
    company = (row.get("company") or "").strip()
    if not company:
        return False, "missing company"
    if company.lower() in EXCLUDE_COMPANIES:
        return False, "already in old list"

    phone = norm_phone(str(row.get("phone") or ""))
    if not phone:
        # try phones list
        for p in row.get("phones") or []:
            phone = norm_phone(str(p))
            if phone:
                break
    if not phone:
        return False, "no real phone"

    if phone in EXCLUDE_PHONES:
        return False, "phone already contacted/old list"

    issues = row.get("website_issues") or row.get("wrong") or ""
    if isinstance(issues, list):
        issues = "; ".join(issues)
    if not is_specific_issue(str(issues)):
        return False, "website issues too generic"

    website = (row.get("website") or "").strip()
    if not website:
        return False, "missing website field"
    # allow explicit no-website leads when issues document marketplace-only presence
    if website.lower() in {"no website", "none", "n/a"} and "no website" not in str(issues).lower() and "zomato" not in str(issues).lower():
        return False, "no website without clear no-website issue"

    owner = (row.get("owner") or row.get("owner_or_dm") or "").strip()
    row["_phone"] = phone
    row["_owner"] = owner
    row["_issues"] = str(issues).strip()
    return True, "ok"


def score(row: dict) -> int:
    s = 0
    if row.get("_owner") and "not found" not in row["_owner"].lower():
        s += 30
    if "@" in (row.get("email") or "") and "not found" not in (row.get("email") or "").lower():
        s += 15
    if row.get("website", "").startswith("http"):
        s += 20
    issues = row.get("_issues", "").lower()
    for k, pts in [
        ("no website", 25),
        ("no online order", 18),
        ("no booking", 18),
        ("gmail", 10),
        ("http", 12),
        ("mobile", 10),
        ("whatsapp", 8),
        ("template", 10),
        ("copyright", 8),
    ]:
        if k in issues:
            s += pts
    s += min(len(row.get("_issues", "")) // 20, 15)
    return s


def draft_whatsapp(row: dict) -> str:
    name = row.get("_owner") or ""
    first = ""
    if name and "not found" not in name.lower():
        first = re.split(r"[\s,/]", name.replace("Dr.", "").replace("Dr ", "").strip())[0]
    greet = f"Hi {first}," if first and len(first) > 1 else "Hello,"
    company = row["company"]
    locality = row.get("locality") or "Navi Mumbai"
    issue = row["_issues"].split(";")[0].strip()
    offer = row.get("offer") or row.get("why_buy") or "a modern website that gets enquiries"
    return (
        f"{greet}\n\n"
        f"I'm Vaibhav from DMC Creatives Studio. I reviewed {company} ({locality}) "
        f"and noticed: {issue}\n\n"
        f"I can share a free one-page redesign / ordering concept for {company} this week — no obligation.\n\n"
        f"Vaibhav Gurav\nDMC Creatives Studio\nwww.dmcstudio.in\n+91 83693 61785"
    )


def draft_email(row: dict) -> tuple[str, str]:
    name = row.get("_owner") or ""
    first = ""
    if name and "not found" not in name.lower():
        first = re.split(r"[\s,/]", name.replace("Dr.", "").replace("Dr ", "").strip())[0]
    greet = f"Dear {first}," if first and len(first) > 1 else "Hello,"
    company = row["company"]
    subject = f"{company}: quick note on your website"
    body = (
        f"{greet}\n\n"
        f"While reviewing businesses in {row.get('locality') or 'Navi Mumbai'}, I looked at {company}.\n\n"
        f"Specific issues I found:\n{row['_issues']}\n\n"
        f"{row.get('why_buy') or 'A clearer website usually converts more calls into booked customers.'}\n\n"
        f"Happy to share a free concept for {company} this week — no obligation.\n\n"
        f"Regards,\nVaibhav Gurav\nDMC Creatives Studio\nhello@dmcstudio.in\nwww.dmcstudio.in\n+91 83693 61785"
    )
    return subject, body


def main() -> None:
    BATCH_DIR.mkdir(exist_ok=True)
    raw = load_batches()
    print(f"Loaded {len(raw)} raw rows from batches")

    qualified: list[dict] = []
    rejected = Counter()
    seen_phones: set[str] = set()
    seen_companies: set[str] = set()

    for row in raw:
        ok, reason = qualify(row)
        if not ok:
            rejected[reason] += 1
            continue
        phone = row["_phone"]
        company_key = row["company"].strip().lower()
        if phone in seen_phones:
            rejected["duplicate phone in new set"] += 1
            continue
        if company_key in seen_companies:
            rejected["duplicate company in new set"] += 1
            continue
        seen_phones.add(phone)
        seen_companies.add(company_key)
        row["score"] = score(row)
        qualified.append(row)

    qualified.sort(key=lambda r: (-r["score"], r["company"].lower()))
    print(f"Qualified: {len(qualified)}")
    print("Rejected:", dict(rejected))

    final = []
    for i, row in enumerate(qualified, 1):
        subject, email_body = draft_email(row)
        wa = draft_whatsapp(row)
        phone = row["_phone"]
        item = {
            "id": i,
            "company": row["company"].strip(),
            "owner": row.get("_owner") or "",
            "phone": display_phone(phone),
            "phone_digits": "91" + phone,
            "email": (row.get("email") or "").strip(),
            "website": (row.get("website") or "").strip(),
            "locality": (row.get("locality") or "").strip(),
            "industry": (row.get("industry") or "").strip(),
            "website_issues": row["_issues"],
            "why_buy": (row.get("why_buy") or row.get("offer") or "").strip(),
            "source": (row.get("source") or row.get("_batch") or "").strip(),
            "score": row["score"],
            "subject": subject,
            "email_body": email_body,
            "whatsapp_msg": wa,
            "wa_link": f"https://wa.me/91{phone}?text=" + __import__("urllib.parse").parse.quote(wa),
            "mailto": (
                f"mailto:{row.get('email')}?subject={__import__('urllib.parse').parse.quote(subject)}"
                f"&body={__import__('urllib.parse').parse.quote(email_body)}"
                if row.get("email") and "@" in row.get("email", "")
                else ""
            ),
            "batch": row.get("_batch", ""),
        }
        final.append(item)

    OUT_JSON.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
    write_xlsx(final)
    print(f"Wrote {len(final)} leads -> {OUT_JSON.name}, {OUT_XLSX.name}")
    with_owner = sum(1 for x in final if x["owner"])
    with_email = sum(1 for x in final if x["email"] and "@" in x["email"])
    print(f"With owner name: {with_owner}/{len(final)} | With email: {with_email}/{len(final)}")


def write_xlsx(rows: list[dict]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Genuine Clients"
    headers = [
        "ID", "Company", "Owner", "Phone", "Email", "Website", "Locality",
        "Industry", "Website Issues (specific)", "Why they'll buy", "Score",
        "WhatsApp Link", "Email Link", "Source",
    ]
    header_fill = PatternFill("solid", fgColor="1F3D2B")
    header_font = Font(color="FFFFFF", bold=True)
    for col, h in enumerate(headers, 1):
        cell = ws.cell(1, col, h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(wrap_text=True, vertical="center")

    for r, row in enumerate(rows, 2):
        vals = [
            row["id"], row["company"], row["owner"], row["phone"], row["email"],
            row["website"], row["locality"], row["industry"], row["website_issues"],
            row["why_buy"], row["score"], row["wa_link"], row["mailto"], row["source"],
        ]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c, v)
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    widths = [5, 28, 22, 16, 28, 34, 22, 16, 48, 36, 8, 18, 18, 24]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:N{len(rows)+1}"
    wb.save(OUT_XLSX)


if __name__ == "__main__":
    main()
