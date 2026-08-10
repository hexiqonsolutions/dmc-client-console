#!/usr/bin/env python3
"""Publish genuine NM leads into the original DMC Client Console UI."""
from __future__ import annotations

import json
from pathlib import Path

import generate_high_value_outreach as hv

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
SRC = ROOT / "genuine_nm_100.json"


def priority_for(score: int) -> str:
    if score >= 70:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"


def map_rows(data: list[dict]) -> list[dict]:
    rows = []
    for r in data:
        phone = (r.get("phone") or "").strip()
        wa = (r.get("phone_digits") or "").strip()
        if not wa and phone:
            digits = "".join(ch for ch in phone if ch.isdigit())
            if digits.startswith("91") and len(digits) >= 12:
                wa = digits[-12:] if len(digits) > 12 else digits
            elif len(digits) == 10:
                wa = "91" + digits
            else:
                wa = digits
        website = (r.get("website") or "").strip()
        issues = (r.get("website_issues") or "").strip()
        why = (r.get("why_buy") or "").strip()
        rows.append(
            {
                "priority": priority_for(int(r.get("score") or 0)),
                "company": r.get("company") or "",
                "industry": r.get("industry") or "",
                "owner_or_dm": r.get("owner") or "",
                "designation": "Owner / Decision maker" if r.get("owner") else "",
                "email": r.get("email") or "",
                "primary_phone_display": phone,
                "phone": phone,
                "website": website,
                "locality": r.get("locality") or "",
                "wrong": issues,
                "offer": why or "Website redesign + enquiry / booking conversion",
                "value_note": why,
                "subject": r.get("subject") or f"{r.get('company')}: quick note on your website",
                "email_body": r.get("email_body") or "",
                "whatsapp_msg": r.get("whatsapp_msg") or "",
                "mailto": r.get("mailto") or "",
                "wa_link": r.get("wa_link") or "",
                "wa_number": wa,
            }
        )
    return rows


def main() -> None:
    data = json.loads(SRC.read_text(encoding="utf-8"))
    rows = map_rows(data)

    # Keep original console UI/path from high-value generator
    out = hv.write_html(rows)

    html = out.read_text(encoding="utf-8")
    html = html.replace(
        "Mumbai + Navi Mumbai + Thane high-value clients with outdated websites. Personalized email & WhatsApp drafts. Signed as Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.",
        "Genuine Navi Mumbai / MMR clients — individually analyzed websites, real phones, old-list excluded. Personalized email & WhatsApp drafts. Signed as Vaibhav Gurav · DMC Creatives · hello@dmcstudio.in · +91 83693 61785.",
    )

    targets = [
        ROOT / "DMC_Client_Console.html",
        ROOT / "Genuine_NM_Console.html",
        REPO / "index.html",  # GitHub Pages
    ]
    for path in targets:
        path.write_text(html, encoding="utf-8")
        print("wrote", path.relative_to(REPO) if path.is_relative_to(REPO) else path)

    print(f"contacts={len(rows)} high={sum(1 for r in rows if r['priority']=='High')} email={sum(1 for r in rows if r['email'])} wa={sum(1 for r in rows if r['wa_number'])}")


if __name__ == "__main__":
    main()
