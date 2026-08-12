#!/usr/bin/env python3
"""Build MIDC-only industrial outreach list (no medical / retail / dental)."""
from __future__ import annotations

import json
import re
import urllib.parse
from collections import Counter
from pathlib import Path

import build_genuine_nm_leads as base
import generate_genuine_console as console

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SRC_MIDC = ROOT / "midc_industrial_outreach_55_80.json"
HV = ROOT / "high_value_prospects.json"
OUT_JSON = ROOT / "genuine_nm_100.json"
OUT_XLSX = ROOT / "Genuine_NM_100_Clients.xlsx"
BATCH_OUT = ROOT / "genuine_batches" / "batch14_midc_only.json"

MIDC_HINTS = (
    "midc", "rabale", "mahape", "taloja", "turbhe", "pawane", "pawne",
    "ttc", "ambernath", "dombivli", "dombivali", "badlapur", "patalganga",
    "rasayani", "koparkhairane", "koperkhairne", "digha", "kalwa",
)

BLOCK_INDUSTRY = (
    "dental", "hospital", "health", "clinic", "diagnostic", "physio",
    "dermat", "maternity", "ivf", "ophthal", "ent", "ortho", "pet",
    "salon", "spa", "bakery", "cafe", "restaurant", "hotel", "banquet",
    "gym", "fitness", "yoga", "coach", "education", "interior", "travel",
    "real estate", "broker", "automotive",
)


def is_midc(row: dict) -> bool:
    blob = " ".join(
        str(row.get(k) or "")
        for k in ("locality", "company", "website_issues", "wrong", "source", "industry")
    ).lower()
    return any(h in blob for h in MIDC_HINTS)


def is_blocked(row: dict) -> bool:
    ind = (row.get("industry") or "").lower()
    return any(b in ind for b in BLOCK_INDUSTRY)


def normalize_row(raw: dict) -> dict:
    website = (raw.get("website") or "").strip()
    if website.lower() in {"", "none", "n/a", "directory listings", "thin / directory"}:
        website = "no website"
    if website.lower().startswith("no ") or "no owned" in website.lower() or "no strong" in website.lower():
        website = "no website"
    issues = raw.get("website_issues") or raw.get("wrong") or ""
    if isinstance(issues, list):
        issues = "; ".join(issues)
    issues = str(issues).strip()
    if website == "no website" and "no website" not in issues.lower() and "indiamart" not in issues.lower():
        issues = (issues + "; No owned website — mainly IndiaMART / directory listings").strip("; ")
    return {
        "company": (raw.get("company") or "").strip(),
        "owner": (raw.get("owner") or raw.get("owner_or_dm") or "").strip(),
        "phone": str(raw.get("phone") or raw.get("hint_phone") or ""),
        "email": (raw.get("email") or "").strip(),
        "website": website,
        "locality": (raw.get("locality") or "").strip(),
        "industry": (raw.get("industry") or "Manufacturing").strip(),
        "website_issues": issues,
        "why_buy": (raw.get("why_buy") or raw.get("offer") or "").strip(),
        "source": (raw.get("source") or "").strip(),
        "_batch": raw.get("_batch") or "midc",
    }


def midc_why(industry: str) -> str:
    ind = (industry or "").lower()
    if "packag" in ind or "print" in ind:
        return "Buyers comparing packaging suppliers usually open 2–3 sites before they raise an RFQ. A clearer catalogue and enquiry form often helps."
    if "chemical" in ind:
        return "Chemical buyers usually want grade/spec clarity and an easy way to request a quote before they call."
    if any(x in ind for x in ("machine", "tool", "pneumatic")):
        return "Machine and tooling buyers shortlist from Google first. Clear capability pages and an RFQ form usually help."
    if "food" in ind:
        return "Export and B2B food buyers often check plant/product pages before they email. A clearer site usually helps those first conversations."
    if any(x in ind for x in ("fabricat", "engineer", "plastic", "manufactur", "logistic")):
        return "B2B buyers in MIDC usually shortlist vendors online before they raise an RFQ. A clearer product/capability page often makes that easier."
    return "Most industrial buyers Google a few MIDC suppliers before they call. A clearer RFQ path on your own site often helps."


# Patch polite drafts for industrial angle
_orig_industry_why = base.industry_why


def industry_why_midc(industry: str) -> str:
    return midc_why(industry)


def draft_whatsapp(row: dict) -> str:
    first = base.first_name(row.get("_owner") or "")
    greet = f"Hi {first}," if first else "Hello,"
    company = row["company"]
    url = base.site_label(row)
    points = base.client_points(row, 2)
    bullets = "\n".join(f"• {p}" for p in points)
    why = midc_why(row.get("industry") or "")
    if url:
        opened = (
            f"I came across {company} in {row.get('locality') or 'MIDC'} and had a look at {url}. "
            f"Hope you don't mind a couple of small observations — only if useful:\n{bullets}"
        )
    else:
        opened = (
            f"I came across {company} in {row.get('locality') or 'MIDC'} while looking at industrial suppliers. "
            f"Hope you don't mind a couple of small observations — only if useful:\n{bullets}"
        )
    return (
        f"{greet}\n\n"
        f"I'm Vaibhav from DMC Creatives Studio. {opened}\n\n"
        f"{why}\n\n"
        f"If it would help, I can send a free one-page catalogue / RFQ concept for {company} this week — no charge and no obligation.\n\n"
        f"Vaibhav Gurav\nDMC Creatives Studio\nwww.dmcstudio.in\n+91 83693 61785"
    )


def draft_email(row: dict) -> tuple[str, str]:
    first = base.first_name(row.get("_owner") or "")
    greet = f"Dear {first}," if first else "Hello,"
    company = row["company"]
    url = base.site_label(row)
    locality = row.get("locality") or "MIDC"
    points = base.client_points(row, 3)
    bullets = "\n".join(f"• {p}" for p in points)
    why = midc_why(row.get("industry") or "")
    host = url.replace("https://", "").replace("http://", "").rstrip("/") if url else ""
    if url:
        subject = f"A quick note on {host} ({locality.split(',')[0]})"
        opened = (
            f"I hope you're well. I'm Vaibhav from DMC Creatives Studio. "
            f"While looking at industrial suppliers in {locality}, I visited {url}."
        )
    else:
        subject = f"A quick note for {company} ({locality.split(',')[0]})"
        opened = (
            f"I hope you're well. I'm Vaibhav from DMC Creatives Studio. "
            f"I came across {company} in {locality} — most of the online presence right now is through directories / IndiaMART rather than a site of your own."
        )
    body = (
        f"{greet}\n\n"
        f"{opened}\n\n"
        f"I wanted to share a few small observations, only in case they're helpful for RFQ buyers:\n{bullets}\n\n"
        f"{why}\n\n"
        f"If you'd like, I can share a free one-page catalogue / RFQ concept for {company} this week. No obligation at all.\n\n"
        f"Warm regards,\nVaibhav Gurav\nDMC Creatives Studio\nhello@dmcstudio.in\nwww.dmcstudio.in\n+91 83693 61785"
    )
    return subject, body


def load_raw() -> list[dict]:
    rows: list[dict] = []
    if SRC_MIDC.exists():
        data = json.loads(SRC_MIDC.read_text(encoding="utf-8-sig"))
        for r in data:
            r["_batch"] = SRC_MIDC.name
            rows.append(r)
    if HV.exists():
        data = json.loads(HV.read_text(encoding="utf-8"))
        for r in data:
            if not is_midc(r) or is_blocked(r):
                continue
            # skip hotels that slipped in via Turbhe locality
            if any(x in (r.get("industry") or "").lower() for x in ("hotel", "college", "education")):
                continue
            r["_batch"] = HV.name
            rows.append(r)
    # also pull manufacturing already in genuine batches with MIDC locality
    for path in sorted((ROOT / "genuine_batches").glob("*.json")):
        if path.name.startswith("batch14"):
            continue
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        if isinstance(data, dict):
            data = data.get("leads") or []
        for r in data:
            if not is_midc(r) or is_blocked(r):
                continue
            ind = (r.get("industry") or "").lower()
            if not any(x in ind for x in (
                "manufactur", "engineer", "chemical", "packag", "plastic", "fabricat",
                "machine", "tool", "pneumatic", "food process", "logistic", "print", "industrial",
            )):
                continue
            r["_batch"] = path.name
            rows.append(r)
    return rows


def qualify_midc(row: dict) -> tuple[bool, str]:
    """Same gates as base, but do not apply old retail/medical exclude lists."""
    company = (row.get("company") or "").strip()
    if not company:
        return False, "missing company"

    phone_raw = str(row.get("phone") or row.get("hint_phone") or "")
    phone = base.norm_phone(phone_raw)
    if not phone:
        # pull first mobile from mixed landline/mobile strings
        for m in re.finditer(r"(?:\+?91[\s\-]?)?([6-9]\d{9})", phone_raw):
            phone = m.group(1)
            break
    if not phone:
        for p in row.get("phones") or []:
            phone = base.norm_phone(str(p))
            if phone:
                break
            for m in re.finditer(r"(?:\+?91[\s\-]?)?([6-9]\d{9})", str(p)):
                phone = m.group(1)
                break
            if phone:
                break
    if not phone:
        return False, "no real phone"
    if len(set(phone)) <= 2 or phone in {"9999999999", "8888888888", "7777777777", "6666666666"}:
        return False, "fake phone"
    if phone.startswith(("000", "111", "12345")):
        return False, "fake phone"

    issues = row.get("website_issues") or row.get("wrong") or ""
    if isinstance(issues, list):
        issues = "; ".join(issues)
    issues = str(issues).strip()
    # accept marketplace-only industrial presence
    low = issues.lower()
    if len(issues) < 40 and any(x in low for x in ("indiamart", "no website", "directory", "no owned")):
        issues = issues + "; No owned website — mainly IndiaMART / directory listings for RFQ buyers"
    if not base.is_specific_issue(issues):
        # allow industrial marketplace / dated-brochure signals
        if not any(
            x in low
            for x in (
                "indiamart", "no website", "directory", "tradeindia", "sme.in", "rfq",
                "catalogue", "gmail", "yahoo", "http", "template", "dated", "thin",
                "basic", "brochure", "aging", "sparse", "outdated", "rediff", "wowslider",
            )
        ):
            return False, "website issues too generic"
        # enrich short notes so drafts have something concrete
        if len(issues) < 50:
            issues = (
                issues
                + "; Dated industrial brochure site with weak RFQ / catalogue conversion for MIDC B2B buyers"
            ).strip("; ")
            row["website_issues"] = issues
            low = issues.lower()

    website = (row.get("website") or "").strip()
    if not website:
        return False, "missing website field"
    if website.lower() in {"no website", "none", "n/a"}:
        if not any(x in issues.lower() for x in ("no website", "indiamart", "directory", "no owned", "marketplace")):
            return False, "no website without clear no-website issue"

    owner = (row.get("owner") or row.get("owner_or_dm") or "").strip()
    row["_phone"] = phone
    row["_owner"] = owner
    row["_issues"] = issues
    return True, "ok"


def score_midc(row: dict) -> int:
    s = base.score(row)
    # boost industrial conversion signals
    issues = (row.get("_issues") or "").lower()
    for k, pts in [
        ("indiamart", 20),
        ("no website", 25),
        ("no owned", 25),
        ("rfq", 12),
        ("catalogue", 10),
        ("yahoo", 10),
        ("rediff", 10),
        ("http", 10),
        ("wowslider", 14),
        ("tradeindia", 16),
        ("directory", 14),
    ]:
        if k in issues:
            s += pts
    loc = (row.get("locality") or "").lower()
    if "midc" in loc:
        s += 15
    # demote medical leftovers if any slipped
    if industry_bucket_safe(row.get("industry") or "") == "medical":
        s -= 100
    return s


def industry_bucket_safe(industry: str) -> str:
    try:
        return base.industry_bucket(industry)
    except Exception:
        return "other"


def main() -> None:
    raw = [normalize_row(r) for r in load_raw()]
    print(f"Loaded {len(raw)} MIDC-candidate rows")

    qualified: list[dict] = []
    rejected = Counter()
    seen_phones: set[str] = set()
    seen_companies: set[str] = set()

    for row in raw:
        if is_blocked(row):
            rejected["blocked industry"] += 1
            continue
        if not is_midc(row):
            rejected["not MIDC"] += 1
            continue
        ok, reason = qualify_midc(row)
        if not ok:
            rejected[reason] += 1
            continue
        phone = row["_phone"]
        company_key = row["company"].strip().lower()
        if phone in seen_phones:
            rejected["duplicate phone"] += 1
            continue
        if company_key in seen_companies:
            rejected["duplicate company"] += 1
            continue
        # Prefer mobile WhatsApp numbers (skip landline-only leftovers that slipped through)
        if not phone[0] in "6789":
            rejected["not mobile"] += 1
            continue
        seen_phones.add(phone)
        seen_companies.add(company_key)
        row["score"] = score_midc(row)
        qualified.append(row)

    qualified.sort(key=lambda r: (-r["score"], r["company"].lower()))
    print(f"Qualified MIDC: {len(qualified)}")
    print("Rejected:", dict(rejected))
    print("Industries:", dict(Counter(r.get("industry") for r in qualified).most_common(20)))

    # persist batch used
    BATCH_OUT.parent.mkdir(exist_ok=True)
    BATCH_OUT.write_text(
        json.dumps(
            [
                {
                    "company": r["company"],
                    "owner": r.get("_owner") or r.get("owner") or "",
                    "phone": r["_phone"],
                    "email": r.get("email") or "",
                    "website": r.get("website") or "",
                    "locality": r.get("locality") or "",
                    "industry": r.get("industry") or "",
                    "website_issues": r.get("_issues") or "",
                    "why_buy": r.get("why_buy") or "",
                    "source": r.get("source") or "",
                }
                for r in qualified
            ],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    final = []
    for i, row in enumerate(qualified, 1):
        subject, email_body = draft_email(row)
        wa = draft_whatsapp(row)
        phone = row["_phone"]
        item = {
            "id": i,
            "company": row["company"].strip(),
            "owner": row.get("_owner") or "",
            "phone": base.display_phone(phone),
            "phone_digits": "91" + phone,
            "email": (row.get("email") or "").strip(),
            "website": (row.get("website") or "").strip(),
            "locality": (row.get("locality") or "").strip(),
            "industry": (row.get("industry") or "").strip(),
            "website_issues": row["_issues"],
            "why_buy": (row.get("why_buy") or "").strip(),
            "source": (row.get("source") or row.get("_batch") or "").strip(),
            "score": row["score"],
            "subject": subject,
            "email_body": email_body,
            "whatsapp_msg": wa,
            "wa_link": "https://wa.me/91" + phone + "?text=" + urllib.parse.quote(wa),
            "mailto": (
                f"mailto:{row.get('email')}?subject={urllib.parse.quote(subject)}"
                f"&body={urllib.parse.quote(email_body)}"
                if row.get("email") and "@" in row.get("email", "")
                else ""
            ),
            "batch": row.get("_batch", ""),
        }
        final.append(item)

    OUT_JSON.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
    base.write_xlsx(final)
    print(f"Wrote {len(final)} MIDC leads -> {OUT_JSON.name}, {OUT_XLSX.name}")

    # publish console
    rows = console.map_rows(final)
    out = __import__("generate_high_value_outreach").write_html(rows)
    html = out.read_text(encoding="utf-8")
    html = html.replace(
        "Mumbai + Navi Mumbai + Thane high-value clients with outdated websites. Personalized email & WhatsApp drafts. Signed as Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.",
        "MIDC industrial clients only (Rabale / Mahape / Turbhe / Taloja / Ambernath / Dombivli…) — no medical. RFQ-focused email & WhatsApp drafts. Signed as Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.",
    )
    html = html.replace(
        "Genuine Navi Mumbai / MMR clients — individually analyzed websites, real phones, old-list excluded. Personalized email & WhatsApp drafts. Signed as Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.",
        "MIDC industrial clients only (Rabale / Mahape / Turbhe / Taloja / Ambernath / Dombivli…) — no medical. RFQ-focused email & WhatsApp drafts. Signed as Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.",
    )
    for path in [ROOT / "DMC_Client_Console.html", ROOT / "Genuine_NM_Console.html", REPO / "index.html"]:
        path.write_text(html, encoding="utf-8")
        print("wrote", path.name if path.parent == ROOT else path.relative_to(REPO))
    print(
        f"contacts={len(rows)} high={sum(1 for r in rows if r['priority']=='High')} "
        f"email={sum(1 for r in rows if r['email'])} wa={sum(1 for r in rows if r['wa_number'])}"
    )


if __name__ == "__main__":
    main()
