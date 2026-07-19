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

LinkedIn Campaign Manager doesn't offer a single export with both full company coverage and lead identity, and there's no self-serve API access — so refreshes combine two Campaign Manager exports, `scripts/gen_linkedin.py`, and one manual step:

1. Export the "companies" report from Campaign Manager twice for the desired window (30/60/90 days — LinkedIn only offers preset windows, and **must match the window size of the previous refresh** — see `is_new` note below): once for the **Ads ad set** (has impressions/clicks) and once for the **InMail ad set** (only has `Paid engagements`, no impressions/clicks).
2. Run `python3 scripts/gen_linkedin.py ads.csv inmail.csv`. It merges the two exports (`views`/`clicks`/`ctr` from Ads only; `engagement` = Ads `Paid engagements` + InMail `Paid engagements`), classifies country/region via `scripts/linkedin_countries.py`, applies the `engagement >= 15`-or-has-a-lead inclusion rule, diffs against the currently committed `data/linkedin.py` for `is_new`, and preserves existing leads.
3. Fix anything the script flags:
   - **NEEDS CLASSIFICATION** — companies not yet in `scripts/linkedin_countries.py`. Look up their country/EMEA base and add them there (Campaign Manager doesn't report country, so this is manual), or add to `EXCLUDED` if there's no clear ICP fit. Re-run.
   - **NEEDS VERIFICATION** comments — best-effort country guesses already in the lookup; worth a sanity check if the company matters to the current decision.
4. Paste the script's `NORTH`/`SOUTH` output into `data/linkedin.py`.
5. Add new leads manually from the separate lead-gen export (name/title/date) — Campaign Manager's company export only gives lead *counts*, not identity. Leads are exempt from the engagement cutoff (kept even if the company's engagement is below 15, or the lead date falls outside the current window) — a submitted lead is real signal regardless of current engagement level.
6. Deploy.

The engagement threshold (default 15 in the script) needs revisiting per refresh since raw totals scale with window size — a 90-day total isn't comparable to a 30-day one, so re-check with `--threshold` if the distribution looks off. Same goes for `is_new`: it's a diff against whatever's currently committed, so it's only meaningful between two refreshes of the *same* window size (the Jul 18 2026 90-day refresh is the current clean baseline).

**Momentum flag (planned, not yet implemented)**: since numbers are windowed snapshots (not cumulative), a future refresh could diff each company's `views`/`engagement` against its value in the previously committed `data/linkedin.py` (via git) and flag significant growth — distinct from `is_new`, which only catches companies absent entirely from the prior list.

## Last updated

- LinkedIn Smart Test data: last 90 days through Jul 18, 2026
- G2 data: Jul 13, 2026 (last 90 days)
