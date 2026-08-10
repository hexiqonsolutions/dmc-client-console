#!/usr/bin/env python3
"""Rebuild seed from Navi Mumbai LEADS, then emit high-value outreach pack."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Users\FPIN\Desktop\dm os\leads")
SOURCE = ROOT / "build_navi_mumbai_leads.py"
SEED = ROOT / "_seed_from_existing.json"


def industry_bucket(ind: str) -> str:
    if any(k in ind for k in ("Manufactur", "Packag", "Print", "EPS", "Plastic", "Metal", "Engineer")):
        return "Manufacturing"
    if any(k in ind for k in ("Hotel", "Hospitality", "Restaurant", "F&B", "Bakery", "Cater")):
        return "Hotel / F&B"
    if any(k in ind for k in ("Health", "Dental", "Clinic", "Diagnostic", "Hospital")):
        return "Healthcare"
    if any(k in ind for k in ("Educat", "Coach", "School")):
        return "Education"
    if any(k in ind for k in ("Auto", "Workshop")):
        return "Automotive"
    if any(k in ind for k in ("Interior", "Architect", "Construct", "Civil", "Builder")):
        return "Real Estate / Design"
    if any(k in ind for k in ("Fitness", "Gym")):
        return "Fitness"
    if any(k in ind for k in ("Travel", "Logistic", "Packer")):
        return "Services"
    return ind.split("—")[0].split("-")[0].strip() or "Business"


def rebuild_seed() -> int:
    src = SOURCE.read_text(encoding="utf-8")
    start = src.index("LEADS = [")
    end = src.index("\nassert len(LEADS)")
    ns: dict = {}
    exec(src[start:end], ns)
    leads = ns["LEADS"]
    email_re = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
    out = []
    for L in leads:
        emails = [e for e in email_re.findall(L.get("email") or "") if "…" not in e]
        phone = L.get("phone") or ""
        low = phone.lower()
        has_phone = phone and "not found" not in low and "gated" not in low and re.search(r"\d{8,}", re.sub(r"\D", "", phone))
        if not emails and not has_phone:
            continue
        pr = L.get("priority", "")
        priority = "High" if ("P1" in pr or "P2" in pr) else "Medium"
        owner = L.get("owner") or ""
        if "not found" in owner.lower():
            owner = ""
        out.append(
            {
                "company": L["company"],
                "owner_or_dm": owner,
                "designation": "",
                "email": emails[0] if emails else "",
                "phone": phone,
                "website": L.get("website") or "",
                "wrong": L.get("wrong") or "",
                "industry": industry_bucket(L.get("industry") or ""),
                "locality": L.get("locality") or "",
                "priority": priority,
                "offer": L.get("offer") or "Website redesign + lead capture",
                "value_note": (L.get("wrong") or "")[:140],
                "source": "navi_mumbai_leads",
            }
        )
    SEED.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(out)


def main() -> None:
    n = rebuild_seed()
    print(f"Seeded {n} from existing Navi Mumbai leads")
    subprocess.check_call([sys.executable, str(ROOT / "generate_high_value_outreach.py")])


if __name__ == "__main__":
    main()
