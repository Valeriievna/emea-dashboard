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
  gen_g2.py                ← Regenerates G2 lists from a new CSV export
  linkedin_countries.py    ← Running company -> (country, region) lookup, reused across LinkedIn refreshes
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
`co, ctry, ch, views, clicks, ctr, engagement, lead, ltitle, ldate, is_new`

- `ch` — list of channels: `"Ads"`, `"InMail"`, `"Demo"`, `"Doc"`, `"Video"`, `"Article"`
- `views`/`clicks`/`ctr` — from the Ads ad-set export only (impressions/clicks aren't reported for InMail)
- `engagement` — combined Ads + InMail `Paid engagements` count (added Jul 18 2026 refresh); `None`/absent on older Unify entries
- `is_new=True` — shows a purple NEW badge (marks companies not present in the previous refresh's NORTH/SOUTH)
- `lead=None` means no lead submitted; non-None rows get a gold highlight (leads are added manually — not derivable from the Campaign Manager company export)

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

## Refreshing LinkedIn data

LinkedIn Campaign Manager doesn't offer a single export with both full company coverage and lead identity, and there's no self-serve API access — so refreshes combine two Campaign Manager exports plus one manual step:

1. Export the "companies" report from Campaign Manager twice for the desired window (30/60/90 days — LinkedIn only offers preset windows): once for the **Ads ad set** (has impressions/clicks) and once for the **InMail ad set** (only has `Paid engagements`, no impressions/clicks).
2. Merge by company name: `views`/`clicks`/`ctr` come only from the Ads export; `engagement` = Ads `Paid engagements` + InMail `Paid engagements`.
3. Classify each company's country and NORTH/SOUTH region (Campaign Manager doesn't report country) — reuse the running lookup built during these sessions rather than re-researching known companies each time. Exclude entries with no clear EMEA base or ICP fit (consumer platforms, academic institutions, unidentifiable "Confidential"/"Stealth" placeholders, negligible signal).
4. Size the list with an `engagement >= 15` floor (combined Ads+InMail engagement) — this replaced an earlier `views >=` cutoff on the Ads side, which let through companies with high impressions but almost no actual interaction. A company with a lead is always kept regardless of engagement. This threshold, like the old one, needs revisiting per refresh since raw totals scale with window size (90-day vs 30-day aren't comparable).
5. `is_new` = not present in the *previous* refresh's `NORTH`/`SOUTH`. **Only diff two refreshes that use the same window size** (e.g. 90-day vs 90-day) — comparing across different window sizes (e.g. this 90-day refresh vs. the prior 30-day one) produces false positives, since a wider window naturally surfaces companies a narrower one wouldn't have shown, even with no real change. The Jul 18 2026 90-day refresh is the current clean baseline with `is_new` cleared on everything; the next refresh (same window size) is what should start populating it again.
6. Leads: Campaign Manager's company export only gives lead *counts*, not names — add `lead`/`ltitle`/`ldate` manually from the per-campaign lead view (its row cap is rarely hit since only a small fraction of engaged companies convert to leads). Keep leads even if the company later drops below the engagement threshold or a submission date falls outside the current window — a lead is real signal regardless of current engagement level.
7. Deploy.

**Momentum flag (planned, not yet implemented)**: since numbers are windowed snapshots (not cumulative), a future refresh could diff each company's `views`/`engagement` against its value in the previously committed `data/linkedin.py` (via git) and flag significant growth — distinct from `is_new`, which only catches companies absent entirely from the prior list.

## Last updated

- LinkedIn Smart Test data: last 90 days through Jul 18, 2026
- G2 data: Jul 13, 2026 (last 90 days)
