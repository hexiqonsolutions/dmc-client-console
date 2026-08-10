#!/usr/bin/env python3
"""Fetch seed URLs, extract contacts carefully, analyze website issues."""
from __future__ import annotations

import json
import re
import ssl
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parent
BATCH_DIR = ROOT / "genuine_batches"
BATCH_DIR.mkdir(exist_ok=True)
SEEDS_FILE = ROOT / "genuine_seeds.json"

UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
}
CTX = ssl.create_default_context()
PHONE_RE = re.compile(r"(?:\+?91[\s\-.]*)?([6-9]\d{9})")
EMAIL_RE = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I)
TEL_RE = re.compile(r"tel:\+?91?[\s\-.]?([6-9]\d{9})", re.I)
WA_RE = re.compile(r"(?:wa\.me|api\.whatsapp\.com/send\?phone=)(?:91)?([6-9]\d{9})", re.I)

# Fallback seeds if genuine_seeds.json missing
DEFAULT_SEEDS = [
    ("Smile Please Dental Clinic", "https://www.smiileplease.com/", "Dental", "Vashi", "Dr. Sharad Kumar", "9821662442"),
    ("Gokhale's Dental Clinic", "https://www.gokhalesdental.in/", "Dental", "Vashi", "Dr. Sunil Gokhale", "9321019134"),
    ("Leela Dental Clinic", "https://leeladental.com/", "Dental", "Kharghar", "Dr. Naveen Acharya", "8976662748"),
    ("The TOOTH Clinic", "https://thetoothclinickharghar.co.in/", "Dental", "Kharghar", "Dr. Bhavna Patel", ""),
    ("FuturistiQ Smiles", "https://futuristiqsmiles.in/", "Dental", "Kharghar", "Dr. Kruti Patel", ""),
    ("Dr Belokar Dental Clinic", "https://drbelokars.com/", "Dental", "Kharghar", "Dr. Belokar", ""),
    ("Elements Dental Clinic", "https://elementsdentalclinic.com/", "Dental", "Vashi", "", ""),
    ("The Dental Studio Kharghar", "https://thedentalstudiokharghar.com/", "Dental", "Kharghar", "Dr. Himmat Jaiswal", ""),
    ("Ora Care Dental Studio", "https://oracaredentalstudio.com/", "Dental", "Kharghar", "Dr. Prerna Malani", ""),
    ("Zellene Dental Care", "https://zellenedentalcare.com/", "Dental", "Kharghar", "Dr. Avishkar Mokal", ""),
    ("Dr Pols Dental Clinic", "https://drpolsdentalclinic.com/", "Dental", "Kharghar", "", ""),
    ("LOMA Dental", "https://lomadental.in/", "Dental", "Vashi", "", ""),
    ("Dentalive", "https://dentalive.in/", "Dental", "Nerul", "", ""),
    ("City Smiles Dental Clinic", "https://citysmiles.in/", "Dental", "Kalamboli", "", ""),
    ("Pulse Dental Clinic", "https://www.pulsedental.in/", "Dental", "Ghansoli", "", ""),
    ("Caramel Bakery", "https://thecaramelbakery.in/", "Bakery", "Kharghar", "", ""),
    ("Munchies Cafe", "https://munchiescafe.co.in/", "Cafe", "Kharghar", "", ""),
    ("Black Fitness Kharghar", "https://blackfitness.co.in/", "Fitness", "Kharghar", "", ""),
    ("Arise Gym Kharghar", "https://arisefitness.in/gym-at-kharghar/", "Fitness", "Kharghar", "", ""),
    ("Equinox Fitness Kharghar", "https://equinoxfitnessindia.com/", "Fitness", "Kharghar", "", ""),
    ("CoreGym Kharghar", "https://coregym.co.in/home", "Fitness", "Kharghar", "", ""),
    ("3D Interiorz", "https://3dinteriorz.com/", "Interior Design", "Kharghar", "Mahesh Ghatge", ""),
    ("Kanchan Kolge Interiors", "https://kanchankolge.com/", "Interior Design", "Vashi", "Kanchan Kolge", ""),
    ("Jyani Interior", "https://jyaniinterior.com/", "Interior Design", "Thane", "Bhanwarlal Jyani", "9224598745"),
    ("Minit Design Studio", "https://minitdesignstudio.com/", "Interior Design", "Thane", "Minit Gandre", "9004506662"),
    ("Studio Elements", "https://studioelements.in/", "Interior Design", "Thane", "Dr. Trupti Shailesh Puranik", "8291996675"),
    ("Alcove Studio", "https://alcovestudio.in/", "Interior Design", "Navi Mumbai", "Sejal Mittal", "9723791721"),
    ("Hotel Aarush", "https://hotelaarush.com/", "Hotel", "CBD Belapur", "", ""),
    ("Hotel Nimantran", "https://nimantranhotel.com/", "Hotel", "CBD Belapur", "", ""),
    ("Hotel Three Star", "https://hotelthreestar.com/", "Hotel", "Kharghar", "", ""),
    ("The Royal Palace Hotel", "https://theroyalpalacehotel.in/", "Hotel", "Vashi", "", ""),
    ("Hotel Pearl", "https://hotelpearlindia.com/", "Hotel", "Vashi", "", ""),
    ("Hotel Victory Inn", "https://hotelvictoryinn.in/", "Hotel", "Vashi", "", ""),
    ("JD's Hotel Rajmahal", "https://jdshotel.com/", "Hotel", "Sanpada", "", ""),
    ("Kaizen Super Specialty Hospital", "https://kaizenhospitals.com/", "Hospital", "Thane", "", ""),
    ("Deodhar Hospital", "https://deodharhospital.com/", "Hospital", "Thane", "Dr. Lalita Deodhar", ""),
    ("Shree Mahavir Jain Hospital", "https://mahavirjainhospital.com/", "Hospital", "Thane", "", ""),
    ("Bethany Hospital", "https://bethanyhospital.in/", "Hospital", "Thane", "", ""),
    ("Tieten Medicity", "https://www.tietenmedicity.com/", "Hospital", "Thane", "", ""),
    ("Infinity IVF and Fertility Center", "https://infinityivf.com/", "Healthcare", "Thane", "", ""),
    ("Thanawala IVF & Maternity Hospital", "https://thanawalamaternity.com/", "Healthcare", "Vashi", "", ""),
    ("Nurture IVF & Fertility Solutions", "https://www.nurtureivfcentre.com/", "Healthcare", "Vashi", "Dr. Sushma Mandava", ""),
    ("Pace IIT & Medical Navi Mumbai", "https://paceiitiansnavimumbai.in/", "Education", "Kharghar", "", ""),
    ("IITians Gravity", "https://www.iitiansgravity.com/", "Education", "Thane", "Shyam Babu Pandey", "9920130144"),
    ("Nucleus IITians Academy", "https://www.nucleusiitiansacademy.com/", "Education", "Nerul", "", ""),
    ("PCMB Edushala", "https://pcmbedushala.com/", "Education", "Vashi", "", ""),
    ("Kharghar Medicity Hospital", "https://www.khargharmedicityhospital.in/", "Hospital", "Kharghar", "", ""),
    ("Rahul Enterprises", "https://rahulenterprises.in/", "Manufacturing", "Rabale", "", ""),
    ("Mahesh Industries", "https://maheshindustries.net.in/", "Manufacturing", "Rabale", "", ""),
]


def is_fake_phone(p: str) -> bool:
    if len(p) != 10 or p[0] not in "6789":
        return True
    if len(set(p)) <= 2:
        return True
    if p in {"9876543210", "9999999999", "9000000000", "9123456789", "9898989898"}:
        return True
    # sequential-ish / repeating blocks
    if p[:5] == p[5:]:
        return True
    if re.fullmatch(r"(\d)\1{9}", p):
        return True
    # reject numbers that look like year/id patterns often scraped from HTML
    if p.startswith(("60", "61", "62", "63", "64", "65", "66")) and p[2:4] in {
        "03",
        "15",
        "20",
        "21",
        "22",
        "23",
        "24",
        "25",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "59",
    }:
        # still allow many real 6x numbers; only reject obvious template junk seen earlier
        if p in {"6603155962", "6035941346", "7333333333", "8571428571"}:
            return True
    if p == "7333333333" or p == "8571428571":
        return True
    return False


def load_seeds() -> list[tuple[str, str, str, str, str, str]]:
    if SEEDS_FILE.exists():
        data = json.loads(SEEDS_FILE.read_text(encoding="utf-8"))
        out = []
        for row in data:
            out.append(
                (
                    row["company"],
                    row["website"],
                    row.get("industry", ""),
                    row.get("locality", "Navi Mumbai"),
                    row.get("owner", ""),
                    row.get("hint_phone", "") or row.get("phone", "") or "",
                )
            )
        return out
    return DEFAULT_SEEDS


def fetch(url: str) -> tuple[str, str, str]:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, context=CTX, timeout=25) as r:
        raw = r.read()
        final = r.geturl()
    text = raw.decode("utf-8", errors="ignore")
    return final, text.lower(), text


def candidate_pages(base: str, html: str) -> list[str]:
    pages = [base]
    parsed = urlparse(base)
    root = f"{parsed.scheme}://{parsed.netloc}/"
    for path in ("contact", "contact-us", "contactus", "about", "about-us", "reach-us"):
        pages.append(urljoin(root, path))
        pages.append(urljoin(root, path + "/"))
        pages.append(urljoin(root, path + ".html"))
        pages.append(urljoin(root, path + ".php"))
    # links from homepage
    for m in re.finditer(r'href=["\']([^"\']*(?:contact|about|reach)[^"\']*)["\']', html, re.I):
        href = m.group(1)
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        pages.append(urljoin(base, href))
    # dedupe preserve order
    seen = set()
    out = []
    for p in pages:
        if p not in seen and p.startswith("http"):
            seen.add(p)
            out.append(p)
    return out[:8]


def extract_phones(html: str, hint: str = "") -> list[str]:
    ranked: list[str] = []
    for m in WA_RE.finditer(html):
        ranked.append(m.group(1))
    for m in TEL_RE.finditer(html):
        ranked.append(m.group(1))
    for m in PHONE_RE.finditer(html):
        ranked.append(m.group(1))
    if hint:
        h = re.sub(r"\D", "", hint)
        if h.startswith("91") and len(h) >= 12:
            h = h[-10:]
        if len(h) == 10:
            ranked.insert(0, h)
    uniq = []
    for p in ranked:
        if is_fake_phone(p):
            continue
        if p not in uniq:
            uniq.append(p)
    return uniq


def extract_emails(html: str) -> list[str]:
    emails = [m.group(0).lower() for m in EMAIL_RE.finditer(html)]
    out = []
    for e in emails:
        if e.endswith((".png", ".jpg", ".webp", ".svg", ".css", ".js")):
            continue
        if any(x in e for x in ("wixpress", "sentry", "example.com", "schema.org", "wordpress", "godaddy")):
            continue
        if e not in out:
            out.append(e)
    return out


def analyze(url: str, html_l: str, html: str) -> list[str]:
    issues: list[str] = []
    if url.startswith("http://"):
        issues.append("Site still on HTTP (no HTTPS trust)")
    if "lorem ipsum" in html_l:
        issues.append("Placeholder Lorem Ipsum content still visible")
    if re.search(r"copyright\s*(©|&copy;)?\s*(20(0|1)\d|2020|2021|2022)", html_l):
        issues.append("Copyright year looks outdated")
    if "@gmail.com" in html_l:
        issues.append("Uses Gmail for business contact (looks less professional)")
    if not any(x in html_l for x in ["whatsapp", "wa.me", "api.whatsapp"]):
        issues.append("No WhatsApp click-to-chat CTA")
    if not any(
        x in html_l
        for x in [
            "book appointment",
            "book now",
            "schedule",
            "reservation",
            "order online",
            "add to cart",
            "book a room",
            "book your",
            "book a visit",
            "online booking",
        ]
    ):
        issues.append("No clear online booking/order path on homepage")
    if "viewport" not in html_l:
        issues.append("Missing mobile viewport meta (weak mobile UX)")
    if "jquery-1." in html_l or "jquery/1." in html_l:
        issues.append("Very old jQuery version detected")
    if len(html) < 9000:
        issues.append("Homepage content is thin / brochure-light")
    if "coming soon" in html_l:
        issues.append("Coming soon / unfinished pages")
    if "000 000 0000" in html_l or "987 828 745" in html_l or "+01-" in html_l:
        issues.append("Fake/placeholder contact numbers visible on site")
    if "indiamart" in html_l and "powered" in html_l:
        issues.append("Looks IndiaMART / marketplace dependent")
    if not issues:
        issues.append("Generic template structure; weak conversion hierarchy vs modern competitors")
    return issues


def main() -> None:
    exclude_path = ROOT / "_exclude_phones.json"
    exclude = set(json.loads(exclude_path.read_text(encoding="utf-8"))) if exclude_path.exists() else set()
    seeds = load_seeds()
    out = []
    seen_companies = set()
    seen_phones = set()

    for company, url, industry, locality, owner, hint in seeds:
        key = company.strip().lower()
        if key in seen_companies:
            continue
        seen_companies.add(key)
        html_all = ""
        final = url
        try:
            final, low, html = fetch(url)
            html_all = html
            # also fetch a couple contact pages
            for page in candidate_pages(final, html)[1:4]:
                try:
                    _, _, h2 = fetch(page)
                    html_all += "\n" + h2
                except Exception:
                    pass
        except Exception as e:
            print("FAIL", company, e)
            continue

        phones = extract_phones(html_all, hint)
        emails = extract_emails(html_all)
        phone = next((p for p in phones if p not in exclude and p not in seen_phones), "")
        if not phone:
            print("NO PHONE", company, phones[:3])
            continue
        seen_phones.add(phone)
        issues = analyze(final, html_all.lower(), html_all)
        row = {
            "company": company,
            "owner": owner,
            "phone": phone,
            "email": emails[0] if emails else "",
            "website": final,
            "locality": f"{locality}, Navi Mumbai" if "mumbai" not in locality.lower() and "thane" not in locality.lower() else locality,
            "industry": industry,
            "website_issues": "; ".join(issues[:4]),
            "why_buy": "Customers shortlist on mobile first — a clearer booking/order site converts more enquiries into paid work.",
            "source": final,
        }
        out.append(row)
        print("OK", company, phone, "|", "; ".join(issues[:2]))

    path = BATCH_DIR / "batch01_verified_seed.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print("wrote", path.name, "count", len(out))


if __name__ == "__main__":
    main()
