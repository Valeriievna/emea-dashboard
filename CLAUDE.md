# EMEA Intent Dashboard

Streamlit app displaying LinkedIn and G2 buyer intent data for EMEA sales.
Live at: https://emea-dashboard-4.streamlit.app (deployed via GitHub → Streamlit Cloud)

## Project structure

```
app.py              ← UI + rendering only (~430 lines)
data/
  linkedin.py       ← NORTH, SOUTH, UNIFY_NORTH, UNIFY_SOUTH (LinkedIn Smart Test + Unify campaigns)
  g2.py             ← G2_NORTH, G2_SOUTH (G2 buyer intent, 49 companies, last 90 days);
                        G2_FM_NORTH, G2_FM_SOUTH (Feature Management product view, 15 companies)
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

## G2 "by product" views

The G2 tab has a PRODUCT selector alongside REGION. `"All Products"` uses `G2_NORTH`/`G2_SOUTH`
(the rules above). `"Feature Management"` uses `G2_FM_NORTH`/`G2_FM_SOUTH` — a narrower view scoped
to one competitive set, built from the raw per-visit-event G2 Buyer Intent CSV export (not the
aggregated export `gen_g2.py` expects — columns include `visit_url`, `visit_type`, `visit_date`,
`visit_title`, `subject_product_name`, etc., one row per visitor page-view).

Differences from the North/South convention above, by design:
- **Competitor scope**: only visits to LaunchDarkly, Unleash, ConfigCat, Statsig, GrowthBook,
  DevCycle, or Optimizely Feature Experimentation count as a signal. (PostHog/VWO Testing/Optimizely
  Web Experimentation are different G2 categories — Product Analytics / A/B Testing — and excluded.)
- **No `signals >= 3` floor for Low** — even a single visit to one of these products is meaningful
  intent for this narrower lens, so all qualifying companies are included regardless of count.
- **Every company gets a `details`/`feed`**, including Low/single-signal ones — the point of this
  view is to let a rep expand any company and see exactly which page views back up the "interest"
  claim, not just to flag High/Medium accounts.
- Country still has to fall in `NORTH_CORE`/`SOUTH_CORE` (same lists as above) or the company is
  dropped rather than redefining territories — this is why Fast Bank (Armenia) and Zenith Bank
  (Nigeria) aren't in the Jul 2026 build even though they had qualifying visits.
- The raw CSV's `company_country`/`company_state` fields aren't always trustworthy (matched by
  domain, not always accurate) — cross-check against `visitor_country`/company identity before
  trusting them blindly. E.g. "The Academic College of Tel Aviv Yaffo" was flagged with
  `company_country=Italy` in the export; it's a real Israeli institution and the visitor was from
  Israel, so it's filed under Israel/South, not Italy.

There's no dedicated regen script for this view yet (built via a one-off scratch script against the
Jul 19 2026 CSV export) — if this becomes a recurring refresh, generalize `scripts/gen_linkedin.py`'s
pattern (a small script parsing the raw CSV, filtering to the competitor slug set, grouping by
company, classifying region) rather than hand-editing `data/g2.py` again.

## G2 detail panels

High and Medium companies can have expandable detail panels. Feed item types:
- `"profile"` → blue dot — viewed a product profile page
- `"category"` → dark gray dot — viewed a category page
- `"compare"` → orange dot — compared two products
- `"alt"` → yellow dot — looked at alternatives to a product

## Refreshing LinkedIn data

LinkedIn Campaign Manager doesn't offer a single export with both full company coverage and lead identity, and there's no self-serve API access — so refreshes combine two Campaign Manager exports, `scripts/gen_linkedin.py`, and one manual step:

1. Export the "companies" report from Campaign Manager twice for the desired window (30/60/90 days — LinkedIn only offers preset windows, and **must match the window size of the previous refresh** — see `is_new` note below): once for the **Ads ad set** (has impressions/clicks) and once for the **InMail ad set** (only has `Paid engagements`, no impressions/clicks).
2. Run `python3 scripts/gen_linkedin.py Ads=ads.csv InMail=inmail.csv` (works for any number of ad-set exports, not just these two — e.g. a Unify-style refresh would be `Doc=doc.csv Video=video.csv Article=article.csv`). It merges all exports (`views`/`clicks`/`ctr` summed across every channel that reports impressions; `engagement` summed across all channels), classifies country/region via `scripts/linkedin_countries.py`, applies the inclusion rule below, diffs against the currently committed `data/linkedin.py` for `is_new`, and preserves existing leads.

**Inclusion rule**: a company with Ads views data is kept if `views >= 150` (clicks aren't separately gated — whatever the real click count is is fine, even 0). A company with *no* Ads views at all (InMail-only) is kept if `engagement >= 15`, since engagement is the only signal available for it. A lead always overrides both. Both numbers (`--views-threshold`, `--engagement-threshold`) need revisiting per refresh since raw totals scale with window size and market (a 90-day EMEA total isn't comparable to a 30-day one, or to NA's much higher-volume market).

**A North America list (`NA`) was tried and removed for now** — it was a flat region (no NORTH_CORE/SOUTH_CORE split), not wired into the script's region classification; would need a small standalone script calling `merge()`, `apply_threshold_and_leads()`, and `load_current(["NA"])` directly if revisited. Always scope `load_current()` to the list(s) you're regenerating — a company can exist as separate entities in different regions under the same name (e.g. Fidelity Investments had both an Ireland and a USA entry), and a lead belongs to one specific entity, not the company name in general.
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
- G2 Feature Management view: Jul 18, 2026 (last 90 days, Apr 21 – Jul 16, 2026 visit window)
