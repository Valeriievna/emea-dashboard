# EMEA Intent Dashboard

Streamlit app displaying LinkedIn and G2 buyer intent data for EMEA sales.
Live at: https://emea-dashboard-4.streamlit.app (deployed via GitHub → Streamlit Cloud)

## Project structure

```
app.py              ← UI + rendering only (~430 lines)
data/
  linkedin.py       ← NORTH, SOUTH, UNIFY_NORTH, UNIFY_SOUTH (LinkedIn Smart Test + Unify campaigns)
  g2.py             ← G2_NORTH, G2_SOUTH (G2 buyer intent, 49 companies, last 90 days)
scripts/
  gen_g2.py         ← Regenerates G2 lists from a new CSV export
requirements.txt
```

## Deploy

**Never push directly to main** — a pre-tool hook blocks it. Always:

```bash
git push origin deploy
SHA=$(git rev-parse deploy)
gh api repos/Valeriievna/emea-dashboard/git/refs/heads/main -X PATCH -f sha=$SHA -F force=true
```

## Data structures

### LinkedIn (data/linkedin.py)

Each entry is a `dict` with keys:
`co, ctry, ch, views, clicks, ctr, op, lead, ltitle, ldate, is_new`

- `ch` — list of channels: `"Ads"`, `"InMail"`, `"Demo"`, `"Doc"`, `"Video"`, `"Article"`
- `is_new=True` — shows a purple NEW badge (marks companies added Jul 1–12 2026)
- `lead=None` means no lead submitted; non-None rows get a gold highlight

### G2 (data/g2.py)

Each entry is a `dict` with keys:
`co, ctry, activity, visitor, last, days, visitors, signals, details`

- `activity` — `"High"` / `"Medium"` / `"Low"`
- `details` — optional dict with `website, hq_full, founded, revenue, employees, feed`
- `feed` items have `type` (`"profile"`, `"category"`, `"compare"`, `"alt"`), `text`, `time`, `loc`
- Low companies included only if `signals >= 3`

### G2 country sets

**NORTH_CORE**: UK, Germany, Netherlands, Sweden, Switzerland, Ireland, Norway, Denmark, Belgium, Luxembourg, Lithuania, Finland, Russia, Russian Federation, Austria, Poland, Czech Republic, Hungary, Romania, Slovakia, Bulgaria, Greece, Latvia, Estonia

**SOUTH_CORE**: France, UAE, Saudi Arabia, Israel, Spain, Italy, Turkey, Türkiye, Croatia, Portugal, Egypt, Morocco, Qatar, Bahrain, Kuwait, Jordan, Cyprus, Lebanon, Tunisia, Algeria

**Skip list**: BCX, UBA Group

## Refreshing G2 data

1. Download new CSV from G2 (buyer intent export, 90-day window)
2. Run `scripts/gen_g2.py` — outputs sorted company lists to stdout
3. Copy the generated `G2_NORTH` and `G2_SOUTH` lists into `data/g2.py`
4. Re-add `details=dict(...)` blocks for High/Medium companies manually (they are hand-curated)
5. Deploy

CSV columns used: `company_name`, `company_country`, `activity_level`, `last_seen`, `competitive_signals`, `visitor_locations`
CSV encoding: `utf-8-sig` (has BOM). Normalize `TÃ¼rkiye` → `Türkiye`.

## G2 detail panels

High and Medium companies can have expandable detail panels. Feed item types:
- `"profile"` → blue dot — viewed a product profile page
- `"category"` → dark gray dot — viewed a category page
- `"compare"` → orange dot — compared two products
- `"alt"` → yellow dot — looked at alternatives to a product

## Last updated

- LinkedIn Smart Test data: Apr 1 – Jul 12, 2026 (23 NEW companies from Jul 1–12 marked with badge)
- G2 data: Jul 13, 2026 (last 90 days)
