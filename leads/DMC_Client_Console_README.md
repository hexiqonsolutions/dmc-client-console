# DMC Client Console — Gulf

BuildView-style one-click outreach for **new Gulf businesses that need a website** and **companies with outdated sites**. Coverage: **UAE, Saudi Arabia, Qatar, Kuwait, Bahrain, Oman**.

Public emails and WhatsApp numbers only — nothing invented.

## Open the app

**Live:** https://hexiqonsolutions.github.io/dmc-client-console/

Or double-click **[DMC_Client_Console.html](./DMC_Client_Console.html)**

## Files

| File | Use |
|---|---|
| `DMC_Client_Console.html` | One-click Email / WhatsApp console |
| `Gulf_Clients.xlsx` | CRM + clickable SEND EMAIL / SEND WHATSAPP |
| `gulf_verified.json` | Source contacts (public pages only) |
| `generate_high_value_outreach.py` | Regenerate drafts + Excel + HTML |

## How to use

1. Filter by country, **New business** vs **Outdated website**, industry, or WhatsApp
2. Click a company → edit the draft if needed
3. **Send Email (1-click)** or **WhatsApp (1-click)**

Signed as **Vaibhav Gurav · DMC Creatives Studio · hello@dmcstudio.in · www.dmcstudio.in · +91 83693 61785**

## Regenerate

```bash
python leads/generate_high_value_outreach.py
```

Requires: `pip install openpyxl`
