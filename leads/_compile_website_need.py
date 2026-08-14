#!/usr/bin/env python3
"""Compile unused + newly verified rows into website_need_research.json. Prints counts only."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHONE_RE = re.compile(r"(?:\+?91[\s\-]?)?([6-9]\d{9})")


def digits_phone(raw) -> str:
    if raw is None:
        return ""
    m = PHONE_RE.search(str(raw).replace(" ", ""))
    if not m:
        d = re.sub(r"\D", "", str(raw))
        if d.startswith("91") and len(d) >= 12:
            d = d[-10:]
        if len(d) == 10 and d[0] in "6789":
            return d
        return ""
    return m.group(1)


def status_from_website(w: str) -> str:
    t = (w or "").lower().strip()
    if not t or t in {"no website", "no own website", "directory / weak web"}:
        return "A — No website"
    if any(x in t for x in ("indiamart", "justdial", "directory", "listing", "zomato", "no website")):
        return "D — Directory only"
    if t.startswith("http"):
        return "B — Poor website"
    return "D — Directory only"


def rec_from_existing(r: dict) -> dict:
    phone = digits_phone(r.get("phone") or r.get("primary_phone"))
    owner = (r.get("owner") or r.get("owner_or_dm") or "").strip()
    website = (r.get("website") or "").strip()
    return {
        "company": (r.get("company") or "").strip(),
        "category": r.get("industry") or r.get("category") or "",
        "locality": r.get("locality") or "",
        "estimated_start_year": r.get("estimated_start_year"),
        "start_year_confidence": r.get("start_year_confidence") or "Unknown — not claimed as 2024–2026 without evidence",
        "website_status": status_from_website(website),
        "website_url": website if website.startswith("http") else "",
        "google_maps": r.get("google_maps") or "",
        "instagram": r.get("instagram") or "",
        "phone": phone,
        "email": (r.get("email") or "").strip() if (r.get("email") or "").lower() not in {"not found publicly", "n/a"} else "",
        "owner": owner,
        "evidence_newness": r.get("evidence_newness") or "Operating industrial/local listing; founding year not verified this round.",
        "website_opportunity": r.get("website_issues") or r.get("wrong") or r.get("why_buy") or "",
        "recommended_website": r.get("offer") or "B2B / service website",
        "source_links": [s for s in [r.get("source"), r.get("website")] if s and str(s).startswith("http")],
        "confidence": "Medium — from prior verified public research; skipped if already contacted",
    }


def main() -> None:
    ex = set(json.loads((ROOT / "_exclude_phones.json").read_text(encoding="utf-8")))
    out = []
    seen = set()
    skipped = {"excluded": 0, "dup": 0, "no_name": 0}

    batches = []
    for fn in ("genuine_nm_100.json", "midc_industrial_outreach_55_80.json"):
        batches.extend(json.loads((ROOT / fn).read_text(encoding="utf-8")))
    extra = json.loads((ROOT / "research_additional_mmr.json").read_text(encoding="utf-8"))
    batches.extend(extra)
    new = json.loads((ROOT / "_new_verified_website_need.json").read_text(encoding="utf-8"))

    def add(row: dict, force_new=False):
        company = (row.get("company") or "").strip()
        if not company:
            skipped["no_name"] += 1
            return
        key = re.sub(r"\W+", "", company.lower())
        if key in seen:
            skipped["dup"] += 1
            return
        phone = digits_phone(row.get("phone"))
        if phone and phone in ex:
            skipped["excluded"] += 1
            return
        seen.add(key)
        if not force_new:
            row = rec_from_existing(row) if "website_opportunity" not in row else row
            row["phone"] = phone or digits_phone(row.get("phone"))
        out.append(row)

    for r in batches:
        add(r)
    for r in new:
        add(r, force_new=True)

    (ROOT / "website_need_research.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print("compiled", len(out))
    print("with_phone", sum(1 for r in out if digits_phone(r.get("phone"))))
    print("named_owner", sum(1 for r in out if (r.get("owner") or "").strip()))
    print("skipped", skipped)


if __name__ == "__main__":
    main()
