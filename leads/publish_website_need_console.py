#!/usr/bin/env python3
"""Rebuild the original DMC Client Console UI with website-need prospects."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import quote

import generate_genuine_console as gc
import generate_high_value_outreach as hv

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SRC = ROOT / "website_need_100.json"


def to_genuine(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        phone = (r.get("phone_display") or r.get("phone") or "").strip()
        digits = "".join(ch for ch in (r.get("phone") or "") if ch.isdigit())
        if len(digits) == 10:
            wa = "91" + digits
        elif digits.startswith("91") and len(digits) >= 12:
            wa = digits[:12] if len(digits) == 12 else "91" + digits[-10:]
        else:
            wa = digits
        website = (r.get("website_url") or "").strip() or (r.get("website_status") or "no website")
        owner = r.get("owner") or ""
        if owner.lower() in {"not identified", "unknown", "n/a"}:
            owner = ""
        wa_msg = (r.get("whatsapp_msg") or "").strip()
        email = (r.get("email") or "").strip()
        subject = f"{r.get('company')}: a quick note on your website"
        email_body = wa_msg.replace("Hi,", "Hello,").replace("Hi ", "Hello ") if wa_msg else ""
        mailto = ""
        if email and email_body:
            mailto = f"mailto:{email}?subject={quote(subject)}&body={quote(email_body)}"
        out.append(
            {
                "company": r.get("company") or "",
                "owner": owner,
                "phone": phone,
                "phone_digits": wa,
                "email": email,
                "website": website,
                "locality": r.get("locality") or "",
                "industry": r.get("category") or "",
                "website_issues": r.get("website_opportunity") or "",
                "why_buy": r.get("recommended_website") or r.get("best_reason") or "",
                "subject": subject,
                "email_body": email_body,
                "whatsapp_msg": wa_msg,
                "mailto": mailto,
                "wa_link": r.get("wa_link") or "",
                "score": int(r.get("lead_score") or 0),
            }
        )
    return out


def main() -> None:
    raw = json.loads(SRC.read_text(encoding="utf-8"))
    rows = gc.map_rows(to_genuine(raw))
    out = hv.write_html(rows)
    html = out.read_text(encoding="utf-8")
    html = html.replace(
        "Mumbai + Navi Mumbai + Thane high-value clients with outdated websites. Personalized email & WhatsApp drafts. Signed as Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.",
        "Website-need prospects — Mumbai / Navi Mumbai / Thane. Same Client Console: list, filters, WhatsApp & email drafts. Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.",
    )
    for path in (
        ROOT / "DMC_Client_Console.html",
        ROOT / "Website_Need_Outreach.html",
        REPO / "index.html",
    ):
        path.write_text(html, encoding="utf-8")
        print("wrote", path.name)
    print("contacts", len(rows), "wa", sum(1 for r in rows if r["wa_number"]))


if __name__ == "__main__":
    main()
