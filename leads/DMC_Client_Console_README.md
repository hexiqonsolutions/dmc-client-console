# DMC Client Console

BuildView-style one-click outreach for outdated-website clients in **Mumbai + Navi Mumbai + Thane**.

## Open the app

Double-click:

**[DMC_Client_Console.html](./DMC_Client_Console.html)**

## Files

| File | Use |
|---|---|
| `DMC_Client_Console.html` | One-click Email / WhatsApp console |
| `High_Value_MMR_Clients.xlsx` | CRM + clickable SEND EMAIL / SEND WHATSAPP |
| `high_value_prospects.json` | Source data |
| `verified_extra_mmr.json` | Researched contacts |
| `generate_high_value_outreach.py` | Regenerate drafts + Excel + HTML |
| `build_high_value_leads.py` | Rebuild seed + regenerate |

## How to use

1. Open `DMC_Client_Console.html` in Chrome
2. Filter by **High**, industry, or “Has WhatsApp”
3. Click a company → edit draft if needed
4. **Send Email (1-click)** or **WhatsApp (1-click)**

Signed as **Vaibhav Gurav · DMC Creatives Studio · hello@dmcstudio.in · www.dmcstudio.in · +91 83693 61785**

## Regenerate

```bash
python leads/build_high_value_leads.py
```

Requires: `pip install openpyxl`
