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


def first_name(owner: str) -> str:
    if not owner or "not found" in owner.lower():
        return ""
    cleaned = re.sub(r"^(Dr\.?|Adv\.?|CA|Mr\.?|Mrs\.?|Ms\.?)\s+", "", owner.strip(), flags=re.I)
    part = re.split(r"[\s,/]", cleaned)[0]
    if len(part) < 2:
        return ""
    # Skip initials like R.R. / A.K.
    if re.fullmatch(r"[A-Za-z]\.?[A-Za-z]\.?", part) or (part.count(".") >= 1 and len(part) <= 5):
        return ""
    return part


def site_label(row: dict) -> str:
    w = (row.get("website") or "").strip()
    if not w.startswith("http"):
        return ""
    w = re.sub(r"/\(S\([^)]+\)\)", "", w)
    m = re.match(r"(https?://[^/\s]+)", w, re.I)
    if not m:
        return w
    host = m.group(1).rstrip("/") + "/"
    path = w[len(m.group(1)) :]
    if not path or path in {"/", "/index.html", "/index.php"} or len(path) > 40 or "ExternalSite" in path or "aspx" in path.lower():
        return host
    return w.split("?")[0].rstrip("/") + ("/" if w.endswith("/") else "")


def split_issues(text: str) -> list[str]:
    parts = re.split(r"[;•\n]+", text or "")
    return [p.strip(" -•").strip() for p in parts if p.strip()]


def plain_issue(raw: str, industry: str = "") -> str:
    """Turn internal audit notes into something a business owner recognises."""
    t = (raw or "").strip()
    low = t.lower()
    ind = (industry or "").lower()

    if "no owned website" in low or low.startswith("no website") or "only zomato" in low or "only swiggy" in low:
        return "You don't have your own website — people only find you on Zomato/Swiggy/Google, so they order there instead of from you"
    if "http 500" in low or "500 error" in low or "intermittently errors" in low or "returns server error" in low or "intermittently 500" in low or "returns 500" in low:
        return "Your website sometimes opens an error page (I got a 500) instead of your homepage"
    if "lorem ipsum" in low:
        return "Placeholder 'Lorem ipsum' dummy text is still visible on the site"
    if "hello world" in low:
        return "A leftover WordPress 'Hello world!' blog post is still live"
    if "stuck at 0" in low or "counters stuck" in low or "0+" in low or "0 locations" in low:
        return "Homepage numbers/stats are stuck at 0 (looks unfinished to visitors)"
    if "copyright" in low and ("2020" in low or "2021" in low or "2022" in low or "outdated" in low or "frozen" in low):
        return "The copyright year on the site is old, so it looks abandoned"
    if "http-only" in low or "still on http" in low or "no https" in low:
        return "The site still opens on HTTP (no lock/HTTPS), which browsers flag as not secure"
    if "@gmail" in low or "gmail-only" in low or "gmail for business" in low or "gmail as" in low or "gmail contact" in low or (
        "gmail" in low and ("email" in low or "contact" in low)
    ):
        return "The public email on the site is a Gmail address, not a company email (e.g. info@yourbrand.in)"
    if "yahoo" in low:
        return "The public email on the site is a Yahoo address — that looks dated to customers"
    if "needhelp@floens" in low or "fake support" in low or ("placeholder" in low and "number" in low):
        return "Leftover template / fake contact details are still showing on the site — not your real number or email"
    if "2012" in low and ("offer" in low or "valid" in low or "march" in low):
        return "Old offers are still live on the site (one still says valid till 2012) — it looks abandoned"
    if "lorem" in low or "mirth large" in low or "unfinished" in low or "[location]" in low:
        return "Unfinished / dummy text is still visible on the live site"
    if "encoding" in low or "mojibake" in low or "glitch" in low:
        return "Reviews/text on the site show broken characters, so it looks unmaintained"
    if "instagram" in low or "facebook" in low and ("broken" in low or "token" in low or "#0" in low):
        return "Social/Instagram links on the site are broken and don't open your real pages"
    if "phone not" in low or "homepage lacks prominent phone" in low or "phone not on homepage" in low:
        return "The phone number is missing from the homepage — people can't call you from the first screen"
    if "no public email" in low or "no visible business email" in low:
        return "There's no business email listed on the site, so serious enquiries have nowhere professional to write"
    if "elementor" in low and ("watermark" in low or "footer" in low):
        return "The footer still shows leftover website-builder / agency watermarks"
    if "viewport" in low or "weak mobile" in low or "mobile ux" in low:
        return "The site is hard to use on a phone — it doesn't fit the screen properly"
    if "wix" in low:
        return "The site is a basic Wix brochure page — it doesn't look like a serious local brand"
    if "swiggy" in low or "zomato" in low:
        return "The site still pushes people to Swiggy/Zomato instead of letting them order/book with you directly"
    if "practo" in low:
        return "The site still sends patients to Practo to book, instead of capturing the appointment on your own page"
    if "template leftovers" in low or "fit365" in low or "luxe haven" in low or "solox" in low or "info@mysite.com" in low:
        return "The site still has leftover template branding that isn't yours"
    if "no whatsapp" in low or "no clear online booking" in low or "no online booking" in low or "call-only" in low or "phone-only" in low or "phone-first" in low:
        if any(x in ind for x in ("dental", "clinic", "hospital", "health", "physio", "salon", "spa")):
            return "There's no clear Book Appointment button — patients have to hunt for a phone number"
        if any(x in ind for x in ("hotel", "banquet", "guest")):
            return "There's no clear Book Room / Check Availability button, so guests go to Booking.com instead"
        if any(x in ind for x in ("bakery", "cafe", "restaurant", "f&b")):
            return "There's no Order Online / Book a table button on the homepage"
        return "There's no clear Book / Enquire button — visitors have to call instead of converting on the site"
    if "no online order" in low or "no cart" in low or "thin menu" in low:
        return "There's no proper online order/menu checkout — people bounce to Swiggy/Zomato"
    if "ota" in low or "direct-booking" in low or "direct booking" in low:
        return "Room/event booking still depends on OTAs instead of a simple booking form on your own site"
    if "google sites" in low:
        return "The site is a basic Google Sites page — not a proper company website for high-ticket work"
    if "typo" in low:
        # keep the actual typo examples if present
        m = re.search(r"['\"]([^'\"]{3,40})['\"]", t)
        if m:
            return f"There are typos on the homepage (e.g. '{m.group(1)}') that look unprofessional"
        return "There are typos on the homepage that look unprofessional"
    if "broken" in low and ("link" in low or "icon" in low or "social" in low or "#0" in low):
        return "Some buttons/links on the site don't go anywhere (broken / leftover links)"
    if "template" in low or "elementor" in low or "wix" in low or "brochure" in low:
        if any(x in ind for x in ("dental", "clinic", "hospital")):
            return "The site looks like a generic clinic template — not a brand patients would trust over a nearby competitor"
        if any(x in ind for x in ("interior",)):
            return "The site looks like SEO/template pages rather than a real project portfolio"
        return "The site looks like a generic template rather than your brand"
    if "thin" in low or "dated" in low or "old html" in low or "php" in low:
        return "The pages look dated and thin — visitors don't get enough proof to call"
    # fallback: shorten but keep meaning
    cleaned = re.sub(r"\s+", " ", t).strip()
    if len(cleaned) > 140:
        cleaned = cleaned[:137].rsplit(" ", 1)[0] + "…"
    return cleaned[0].upper() + cleaned[1:] if cleaned else t


def industry_why(industry: str) -> str:
    ind = (industry or "").lower()
    if "dental" in ind:
        return "Patients Google a dentist, open 2–3 sites, and book the one that looks easiest. Right now yours makes them call and wait."
    if any(x in ind for x in ("hospital", "health", "physio", "ivf", "diagnostic", "maternity", "dermat")):
        return "Patients compare clinics on their phone before they call. A clearer booking page usually wins the appointment."
    if any(x in ind for x in ("bakery", "cafe", "restaurant", "f&b", "cater")):
        return "Hungry customers open your site to order or book a table. If that's hard, they go to Zomato/Swiggy and you lose the margin."
    if any(x in ind for x in ("hotel", "banquet", "guest")):
        return "Guests who land on your site should be able to check dates and book. If they can't, they pay Booking.com instead of you."
    if "interior" in ind:
        return "Homeowners shortlist 3 designers from Google. A clear project gallery + quote form gets the site visit."
    if any(x in ind for x in ("gym", "fitness", "yoga", "salon", "spa", "beauty")):
        return "People decide memberships/appointments from the phone. If trial/booking isn't obvious, they join the competitor who made it easy."
    if any(x in ind for x in ("coach", "education", "tutor")):
        return "Parents compare institutes online. A demo-class / admission form on the site captures the enquiry before they call someone else."
    if any(x in ind for x in ("packers", "travel", "real estate", "broker")):
        return "High-ticket buyers want a trustworthy site with a quote form — directory pages make them hesitate."
    return "People who find you on Google decide in a few seconds whether to enquire. The site should make that one tap, not a hunt."


def client_points(row: dict, limit: int = 3) -> list[str]:
    industry = row.get("industry") or ""
    seen = set()
    out = []
    for raw in split_issues(row.get("_issues") or ""):
        p = plain_issue(raw, industry)
        key = p.lower()
        if key in seen or len(p) < 20:
            continue
        seen.add(key)
        out.append(p)
        if len(out) >= limit:
            break
    return out or [plain_issue(row.get("_issues") or "", industry)]


def draft_whatsapp(row: dict) -> str:
    first = first_name(row.get("_owner") or "")
    greet = f"Hi {first}," if first else "Hello,"
    company = row["company"]
    url = site_label(row)
    points = client_points(row, 2)
    bullets = "\n".join(f"• {p}" for p in points)
    why = industry_why(row.get("industry") or "")
    if url:
        opened = f"I opened your website ({url}) and a couple of things stood out:\n{bullets}"
    else:
        opened = f"I searched for {company} online and a couple of things stood out:\n{bullets}"
    return (
        f"{greet}\n\n"
        f"I'm Vaibhav from DMC Creatives Studio. {opened}\n\n"
        f"{why}\n\n"
        f"I can send a free one-page concept for {company} this week so you can see the difference — no charge, no obligation.\n\n"
        f"Vaibhav Gurav\nDMC Creatives Studio\nwww.dmcstudio.in\n+91 83693 61785"
    )


def draft_email(row: dict) -> tuple[str, str]:
    first = first_name(row.get("_owner") or "")
    greet = f"Dear {first}," if first else "Hello,"
    company = row["company"]
    url = site_label(row)
    locality = row.get("locality") or "Navi Mumbai"
    points = client_points(row, 3)
    bullets = "\n".join(f"• {p}" for p in points)
    why = industry_why(row.get("industry") or "")
    if url:
        subject = f"{company}: I checked {url.replace('https://','').replace('http://','').rstrip('/')}"
        opened = f"I opened {url} while looking at {industry_label_short(row.get('industry') or 'local')} businesses in {locality}."
    else:
        subject = f"{company}: no website of your own yet"
        opened = f"I searched for {company} in {locality} — there's no owned website, only listings."
    body = (
        f"{greet}\n\n"
        f"{opened}\n\n"
        f"Here's what a customer would notice today:\n{bullets}\n\n"
        f"{why}\n\n"
        f"I can share a free concept page for {company} this week so it's clear what I'd change — no obligation.\n\n"
        f"Regards,\nVaibhav Gurav\nDMC Creatives Studio\nhello@dmcstudio.in\nwww.dmcstudio.in\n+91 83693 61785"
    )
    return subject, body


def industry_label_short(industry: str) -> str:
    return (industry or "local").split("/")[0].strip().lower() or "local"


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
        "Email Subject", "Email Body", "WhatsApp Message",
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
            row["why_buy"], row["score"], row.get("subject") or "", row.get("email_body") or "",
            row.get("whatsapp_msg") or "", row["wa_link"], row["mailto"], row["source"],
        ]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c, v)
            cell.alignment = Alignment(wrap_text=True, vertical="top")

    widths = [5, 28, 22, 16, 28, 34, 22, 16, 48, 36, 8, 36, 48, 48, 18, 18, 24]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:N{len(rows)+1}"
    wb.save(OUT_XLSX)


if __name__ == "__main__":
    main()
