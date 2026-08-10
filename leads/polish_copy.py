#!/usr/bin/env python3
"""Professional outreach copy + eye-catching subjects for all leads."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"C:\Users\FPIN\Desktop\dm os\leads")
SOURCE = ROOT / "build_navi_mumbai_leads.py"


def greeting_name(owner: str) -> str | None:
    if not owner:
        return None
    low = owner.lower()
    if "not found" in low:
        return None
    part = re.split(r"[/(,]", owner)[0].strip()
    part = re.sub(
        r"^(Dr\.?|Adv\.?|CA|Mr\.?|Mrs\.?|Ms\.?|Shri|Smt\.?)\s+",
        "",
        part,
        flags=re.I,
    ).strip()
    # Prefer a clean human name token (skip "CEO", "Partner")
    tokens = [t for t in part.split() if t.lower() not in {"ceo", "md", "director", "partner", "proprietor", "manager", "and", "&"}]
    if not tokens:
        return None
    # Use first name for warmth; keep short
    name = tokens[0]
    if len(name) < 2:
        return None
    return name


def short_area(locality: str) -> str:
    if not locality:
        return "Navi Mumbai"
    # Take primary area before parenthesis
    area = locality.split("(")[0].strip()
    area = re.split(r"[/–—-]", area)[0].strip()
    return area or "Navi Mumbai"


def industry_label(industry: str) -> str:
    if "—" in industry:
        return industry.split("—", 1)[1].strip().lower()
    if "-" in industry:
        return industry.split("-", 1)[-1].strip().lower()
    return industry.lower()


def hook_line(lead: dict) -> str:
    wrong = (lead.get("wrong") or "").strip()
    company = lead["company"]
    priority = lead.get("priority", "")

    # Prefer crisp hooks by priority pattern
    wlow = wrong.lower()
    if "P1" in priority or "no website" in wlow or "no own" in wlow or "justdial" in wlow or "indiamart only" in wlow or "directory only" in wlow or "zomato only" in wlow:
        if "indiamart" in wlow:
            return f"{company} is easy to find on IndiaMART, but there is still no company website buyers can trust."
        if "justdial" in wlow or "practo" in wlow or "zomato" in wlow or "directory" in wlow:
            return f"{company} still depends on directory/marketplace listings instead of an owned website."
        if "gmail" in wlow or "hotmail" in wlow or "rediff" in wlow or "yahoo" in wlow:
            return f"{company}'s public contact still looks outdated (personal email / weak web presence)."
        return f"{company} does not yet have a professional website of its own."

    if "http" in wlow and "https" not in wlow.replace("https", ""):
        return f"{company}'s website is still on HTTP and feels dated for serious buyers."
    if "template" in wlow or "indiamart catalog" in wlow or "tradeindia" in wlow:
        return f"{company}'s current site still looks like a marketplace template — not a brand site."
    if "outdated" in wlow or "dated" in wlow or "old" in wlow or "thin" in wlow or "basic" in wlow or "wowslider" in wlow or "©2020" in wrong or "2008" in wrong:
        return f"I reviewed {company}'s website — it works, but it no longer looks current or conversion-ready."
    if "booking" in wlow or "crm" in wlow or "phone" in wlow:
        return f"{company} has a website, but enquiries still rely heavily on phone/WhatsApp with little follow-up structure."
    # Fallback: first sentence of wrong, cleaned
    first = re.split(r"(?<=[.!?])\s+", wrong)[0].strip()
    if first and len(first) < 160:
        return first
    return f"I reviewed {company}'s online presence and spotted a clear gap versus stronger local competitors."


def value_line(lead: dict) -> str:
    offer = (lead.get("offer") or "").lower()
    industry = industry_label(lead.get("industry", ""))
    if "crm" in offer and "website" in offer:
        return "We help Navi Mumbai businesses fix this with a clean website first, then optional enquiry CRM / invoicing if useful."
    if "booking" in offer or "appointment" in offer:
        return "We design simple, mobile-first sites with clear booking/enquiry paths — built for local clients, not generic templates."
    if "portfolio" in offer:
        return "We build portfolio-led websites that turn browsers into serious enquiries."
    if "catalogue" in offer or "catalog" in offer or "rfq" in offer:
        return "We build B2B catalogue sites with clear product pages and RFQ forms so serious buyers can shortlist you faster."
    if "invoice" in offer or "dashboard" in offer or "portal" in offer or "membership" in offer:
        return "After the website, we can add light CRM, invoicing, or a simple dashboard — only if you need it."
    if "manufacturing" in lead.get("industry", "").lower() or "packaging" in industry or "engineering" in industry:
        return "We specialise in manufacturer websites across Mahape, Rabale, Turbhe and Taloja — practical, mobile-ready, enquiry-focused."
    return "We build professional websites for Navi Mumbai businesses — clear, mobile-ready, and focused on enquiries."


def cta_line(company: str) -> str:
    return f"If helpful, I can share a free one-page concept for {company} this week — no obligation."


def professional_message(lead: dict) -> str:
    name = greeting_name(lead.get("owner", ""))
    company = lead["company"]
    area = short_area(lead.get("locality", ""))
    niche = industry_label(lead.get("industry", ""))

    hello = f"Dear {name}," if name else "Hello,"
    intro = f"While reviewing {niche} businesses in {area}, I came across {company}."
    hook = hook_line(lead)
    value = value_line(lead)
    cta = cta_line(company)

    return "\n\n".join(
        [
            hello,
            intro,
            hook,
            value,
            cta,
            "Regards,\nVaibhav Gurav\nDMC Creatives Studio\nwww.dmcstudio.in\n+91 83693 61785",
        ]
    )


def eye_catchy_subject(lead: dict) -> str:
    company = lead["company"]
    area = short_area(lead.get("locality", ""))
    priority = lead.get("priority", "")
    wrong = (lead.get("wrong") or "").lower()
    industry = industry_label(lead.get("industry", ""))

    # Rotate patterns by company hash for variety but determinism
    patterns_p1 = [
        f"{company}: still invisible beyond directories?",
        f"Why {company} may be losing enquiries in {area}",
        f"{company} — no website yet. Competitors already have one.",
        f"Quick question for {company} ({area})",
        f"{company}: buyers search Google before they call",
    ]
    patterns_p2 = [
        f"Noticed this on {company}'s website",
        f"{company}'s site looks outdated — easy fix, big difference",
        f"One update that could lift enquiries for {company}",
        f"{company} ({area}): website audit in 60 seconds",
        f"Your {industry} site may be costing you leads",
    ]
    patterns_p3 = [
        f"{company}: website is fine — follow-up is the gap",
        f"Stop losing {company} enquiries after the first call",
        f"{company} — ready for CRM / booking / invoicing?",
        f"Small systems upgrade for {company} ({area})",
        f"After the click: how {company} can close more leads",
    ]

    if "indiamart" in wrong and ("no" in wrong or "only" in wrong or "primarily" in wrong):
        return f"{company} is on IndiaMART — but buyers want your website"
    if "justdial" in wrong and "no" in wrong:
        return f"{company}: JustDial alone won't win serious clients"
    if "still on http" in wrong or "runs on http" in wrong or "http site" in wrong or "(http," in wrong:
        return f"{company}.in is still on HTTP — that hurts trust"
    if "wowslider" in wrong or "2008" in wrong:
        return f"{company}'s website still looks stuck in the past"
    if "template" in wrong:
        return f"{company}: template site vs brand site — buyers can tell"

    idx = sum(ord(c) for c in company) % 5
    if "P1" in priority:
        return patterns_p1[idx]
    if "P3" in priority:
        return patterns_p3[idx]
    return patterns_p2[idx]


def polish_all_leads(leads: list[dict]) -> list[dict]:
    out = []
    for lead in leads:
        updated = dict(lead)
        updated["outreach"] = professional_message(lead)
        updated["subject"] = eye_catchy_subject(lead)
        out.append(updated)
    return out


def patch_source_file() -> None:
    """Rewrite outreach strings in build_navi_mumbai_leads.py and inject subject keys."""
    src = SOURCE.read_text(encoding="utf-8")
    start = src.index("LEADS = [")
    end = src.index("\nassert len(LEADS)")
    ns: dict = {}
    exec(src[start:end], ns)
    polished = polish_all_leads(ns["LEADS"])

    # Rebuild LEADS literal carefully via repr of dicts (stable keys order)
    lines = ["LEADS = ["]
    for lead in polished:
        lines.append("  {")
        for key in [
            "company",
            "owner",
            "email",
            "phone",
            "website",
            "wrong",
            "industry",
            "priority",
            "locality",
            "offer",
            "subject",
            "outreach",
        ]:
            val = lead[key]
            lines.append(f'    "{key}": {val!r},')
        lines.append("  },")
    lines.append("]")
    new_block = "\n".join(lines)
    SOURCE.write_text(src[:start] + new_block + src[end:], encoding="utf-8")
    print(f"Patched {len(polished)} leads in {SOURCE.name}")


if __name__ == "__main__":
    patch_source_file()
