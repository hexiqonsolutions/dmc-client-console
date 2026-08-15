#!/usr/bin/env python3
"""Rebuild the original DMC Client Console with clean names and full drafts."""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import quote

import build_genuine_nm_leads as base
import generate_genuine_console as gc
import generate_high_value_outreach as hv

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
FRESH = ROOT / "fresh_launch_prospects.json"

SKIP_COMPANY = (
    "apollo clinic",
    "metropolis healthcare",
    "haware",
    "navnit motors",
    "modi hyundai",
    "pace iit",
    "iitians gravity",
    "nucleus iitians",
    "kaizergsm",
    "shivam autozone",
    "fortpoint",
    "excell autovista",
    "kiran motors",
    "sanghi auto",
)

JUNK_OWNER = {
    "",
    "not identified",
    "unknown",
    "n/a",
    "not found publicly",
    "not found",
}


def skip_company(name: str) -> bool:
    n = (name or "").lower()
    return any(s in n for s in SKIP_COMPANY)


def company_key(name: str) -> str:
    return re.sub(r"\W+", "", (name or "").lower())


def clean_owner(raw: str) -> str:
    if not raw or raw.strip().lower() in JUNK_OWNER:
        return ""
    part = re.split(r"[/(,]", raw)[0].strip()
    part = re.sub(
        r"^(Dr\.?|Adv\.?|CA|Mr\.?|Mrs\.?|Ms\.?|Shri|Smt\.?)\s+",
        "",
        part,
        flags=re.I,
    ).strip()
    # Rajeev / Rajiv already split; leftover "Rajeev"
    tokens = []
    for t in part.split():
        if t.lower() in {"ceo", "md", "director", "partner", "proprietor", "manager", "and", "&"}:
            continue
        if re.fullmatch(r"[A-Za-z]\.?", t):
            tokens.append(t[0].upper() + ".")
            continue
        # KamalNain -> Kamalnain
        if re.search(r"[a-z][A-Z]", t):
            t = t[0] + t[1:].lower() if t[0].isupper() else t.lower()
        elif t.isupper() and len(t) > 3:
            t = t.title()
        tokens.append(t)
    name = " ".join(tokens).strip()
    return name


def greet_first(owner: str) -> str:
    if not owner:
        return ""
    words = [t for t in owner.split() if not re.fullmatch(r"[A-Za-z]\.", t)]
    if not words:
        return ""
    first = words[0]
    if len(first) < 2:
        return ""
    return first


def site_url(website: str) -> str:
    w = (website or "").strip()
    if w.startswith("http"):
        return w
    return ""


def bullets(issues: str, website: str) -> list[str]:
    points = []
    t = (issues or "").strip()
    if t:
        first = re.split(r"(?<=[.!?])\s+", t)[0].strip().rstrip(".")
        if first:
            points.append(first[:180])
    w = (website or "").lower()
    if not site_url(website) or "no website" in w or w.startswith("a") or w.startswith("c") or w.startswith("d"):
        points.append("Most people currently find you on listings (Google / IndiaMART) rather than a site of your own")
    else:
        points.append("The pages are a little light on detail — more proof (photos, services, RFQ) usually helps people feel ready to call")
    # unique, max 2
    out, seen = [], set()
    for p in points:
        k = p.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(p)
        if len(out) == 2:
            break
    return out or ["A clearer website would make it easier for buyers to shortlist you."]


def why_line(industry: str) -> str:
    ind = (industry or "").lower()
    if any(x in ind for x in ("cafe", "bakery", "restaurant", "salon")):
        return "Guests usually check a website for menu, hours and location before they visit or message."
    if any(x in ind for x in ("packag", "print")):
        return "Buyers comparing packaging suppliers usually open 2–3 sites before they raise an RFQ. A clearer catalogue and enquiry form often helps."
    if any(x in ind for x in ("fabricat", "engineer", "manufact", "machine", "plastic", "chemical")):
        return "B2B buyers in MIDC usually shortlist vendors online before they raise an RFQ. A clearer product/capability page often makes that easier."
    if "waterproof" in ind or "contractor" in ind:
        return "Homeowners and societies usually Google waterproofing / civil work and pick the contractor with clear project photos and an easy enquiry path."
    return "Most buyers Google a few local suppliers before they call. A clearer enquiry path on your own site often helps."


def draft_whatsapp(company: str, owner: str, locality: str, website: str, issues: str, industry: str) -> str:
    first = greet_first(owner)
    greet = f"Hi {first}," if first else "Hello,"
    url = site_url(website)
    area = locality or "Navi Mumbai"
    pts = "\n".join(f"• {p}" for p in bullets(issues, website))
    why = why_line(industry)
    if url:
        opened = (
            f"I came across {company} in {area} and had a look at {url}. "
            f"Hope you don't mind a couple of small observations — only if useful:\n{pts}"
        )
    else:
        opened = (
            f"I came across {company} in {area} while looking at local businesses. "
            f"Hope you don't mind a couple of small observations — only if useful:\n{pts}"
        )
    return (
        f"{greet}\n\n"
        f"Happy Independence Day to you and the team at {company}.\n\n"
        f"I'm Vaibhav from DMC Creatives Studio. {opened}\n\n"
        f"{why}\n\n"
        f"If it would help, I can send a free one-page concept for {company} this week — no charge and no obligation.\n\n"
        f"Vaibhav Gurav\nDMC Creatives Studio\nwww.dmcstudio.in\n+91 83693 61785"
    )


def draft_email(company: str, owner: str, locality: str, website: str, issues: str, industry: str) -> tuple[str, str]:
    first = greet_first(owner)
    greet = f"Dear {first}," if first else "Hello,"
    url = site_url(website)
    area = locality or "Navi Mumbai"
    pts = "\n".join(f"• {p}" for p in bullets(issues, website))
    why = why_line(industry)
    host = url.replace("https://", "").replace("http://", "").rstrip("/") if url else ""
    if url:
        subject = f"A quick note on {host.split('/')[0]} ({area.split(',')[0]})"
        opened = (
            f"I hope you're well. I'm Vaibhav from DMC Creatives Studio. "
            f"While looking at businesses in {area}, I visited {url}."
        )
    else:
        subject = f"A quick note for {company} ({area.split(',')[0]})"
        opened = (
            f"I hope you're well. I'm Vaibhav from DMC Creatives Studio. "
            f"I came across {company} in {area} — most of the online presence right now is through directories rather than a site of your own."
        )
    body = (
        f"{greet}\n\n"
        f"Wishing you a happy Independence Day.\n\n"
        f"{opened}\n\n"
        f"I wanted to share a few small observations, only in case they're helpful:\n{pts}\n\n"
        f"{why}\n\n"
        f"If you'd like, I can share a free one-page concept for {company} this week. No obligation at all.\n\n"
        f"Warm regards,\nVaibhav Gurav\nDMC Creatives Studio\nhello@dmcstudio.in\nwww.dmcstudio.in\n+91 83693 61785"
    )
    return subject, body


def phone_digits(raw: str) -> str:
    d = re.sub(r"\D", "", raw or "")
    if d.startswith("91") and len(d) >= 12:
        d = d[-10:]
    if len(d) == 10 and d[0] in "6789":
        return d
    return ""


def display_phone(p: str) -> str:
    return f"+91 {p[:5]} {p[5:]}" if len(p) == 10 else ""


def as_console_row(r: dict, *, keep_drafts: bool) -> dict | None:
    company = (r.get("company") or "").strip()
    if not company or skip_company(company):
        return None
    owner = clean_owner(r.get("owner") or r.get("owner_or_dm") or "")
    phone = phone_digits(r.get("phone") or r.get("phone_display") or "")
    email = (r.get("email") or "").strip()
    if email.lower() in JUNK_OWNER:
        email = ""
    website = site_url(r.get("website") or r.get("website_url") or "") or "no website"
    locality = (r.get("locality") or "").strip()
    industry = (r.get("industry") or r.get("category") or "").strip()
    issues = (r.get("website_issues") or r.get("website_opportunity") or r.get("wrong") or "").strip()
    why = (r.get("why_buy") or r.get("recommended_website") or r.get("offer") or "").strip()
    wa_msg = (r.get("whatsapp_msg") or "").strip() if keep_drafts else ""
    email_body = (r.get("email_body") or "").strip() if keep_drafts else ""
    subject = (r.get("subject") or "").strip() if keep_drafts else ""
    if not wa_msg or len(wa_msg) < 80:
        wa_msg = draft_whatsapp(company, owner, locality, website, issues, industry)
    if not email_body or len(email_body) < 80:
        subject, email_body = draft_email(company, owner, locality, website, issues, industry)
    elif not subject:
        subject = f"A quick note for {company}"
    wa = "91" + phone if phone else ""
    mailto = ""
    if email:
        mailto = f"mailto:{email}?subject={quote(subject)}&body={quote(email_body)}"
    wa_link = f"https://wa.me/{wa}?text={quote(wa_msg)}" if wa else ""
    return {
        "company": company,
        "owner": owner,
        "phone": display_phone(phone) if phone else "",
        "phone_digits": wa,
        "email": email,
        "website": website,
        "locality": locality,
        "industry": industry,
        "website_issues": issues,
        "why_buy": why or "Website + enquiry conversion",
        "subject": subject,
        "email_body": email_body,
        "whatsapp_msg": wa_msg,
        "mailto": mailto,
        "wa_link": wa_link,
        "score": int(r.get("score") or r.get("lead_score") or 60),
    }


def main() -> None:
    fresh = json.loads(FRESH.read_text(encoding="utf-8"))
    seen = set()
    merged: list[dict] = []
    for raw in fresh:
        row = as_console_row(raw, keep_drafts=False)
        if not row:
            continue
        key = company_key(row["company"])
        if key in seen:
            continue
        seen.add(key)
        merged.append(row)

    # Named + phone first, then named, then the rest
    def rank(r: dict) -> tuple:
        named = 1 if r["owner"] else 0
        ph = 1 if r["phone_digits"] else 0
        return (-named, -ph, -r["score"], r["company"])

    merged.sort(key=rank)
    rows = gc.map_rows(merged)
    out = hv.write_html(rows)
    html = out.read_text(encoding="utf-8")
    html = html.replace(
        "Mumbai + Navi Mumbai + Thane high-value clients with outdated websites. Personalized email & WhatsApp drafts. Signed as Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.",
        "New interiors, shops and launches in Mumbai / Navi Mumbai / Thane — weak or missing websites only. Independence Day wish on every draft. Vaibhav Gurav · DMC Creatives · +91 83693 61785.",
    )
    for path in (
        ROOT / "DMC_Client_Console.html",
        ROOT / "Website_Need_Outreach.html",
        REPO / "index.html",
    ):
        path.write_text(html, encoding="utf-8")
        print("wrote", path.name)

    named = sum(1 for r in rows if r["owner_or_dm"])
    drafted = sum(1 for r in rows if len(r["whatsapp_msg"]) > 80)
    print(
        "contacts",
        len(rows),
        "named",
        named,
        "drafts",
        drafted,
        "wa",
        sum(1 for r in rows if r["wa_number"]),
    )


if __name__ == "__main__":
    main()
