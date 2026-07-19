"""
Regenerate LinkedIn NORTH/SOUTH from N Campaign Manager "companies" exports
(same window size, e.g. all 90-day) — one per ad set. Works for Smart Test
(2 ad sets: Ads, InMail) or campaigns with more ad sets, like Unify
(Doc, Video, Article), or anything in between.

Usage:
    python3 scripts/gen_linkedin.py Ads=ads.csv InMail=inmail.csv [--views-threshold 150] [--engagement-threshold 15]
    python3 scripts/gen_linkedin.py Doc=doc.csv Video=video.csv Article=article.csv

What it does:
    1. Merges all N exports by company name.
       - views/clicks/ctr = summed Paid impressions/clicks across every
         channel that reports them (some, like InMail, never do).
       - engagement = summed Paid engagements across every channel.
       - ch = list of channel names the company showed real signal in
         (impressions or engagements), e.g. ["Ads","InMail"] or
         ["Doc","Video"].
    2. Classifies country/region using scripts/linkedin_countries.py (the
       running lookup). Companies not in that lookup are printed separately
       under NEEDS CLASSIFICATION — add them to linkedin_countries.py by hand
       (LinkedIn's export doesn't report company country) and re-run.
    3. Keeps a company if: it has Ads views >= views-threshold (default 150,
       clicks aren't separately gated — whatever the real click count is is
       fine); OR, for InMail-only companies with no Ads views at all,
       engagement >= engagement-threshold (default 15); OR it already has a
       lead in the currently committed data/linkedin.py.
    4. Computes is_new by diffing against the currently committed NORTH/SOUTH
       in data/linkedin.py. Only meaningful if the previous refresh used the
       SAME window size (30 vs 90-day totals aren't comparable).
    5. Preserves lead/ltitle/ldate from the currently committed data for any
       company that already has one (add new leads by hand afterward from the
       separate lead-gen export, since Campaign Manager's company export only
       gives lead counts, not identity).
    6. Prints ready-to-paste NORTH/SOUTH blocks to stdout.

NA (North America, flat region, no EMEA-style NORTH_CORE/SOUTH_CORE split) isn't
wired into main()'s classify() step — regenerate it with a small standalone
script calling merge(), apply_threshold_and_leads(), and load_current(["NA"])
directly. Always pass load_current() the list(s) matching what you're
regenerating — a company can exist as separate entities in different regions
under the same name (e.g. "Fidelity Investments" in both NA and EMEA), and a
lead belongs to one specific entity, not the company name in general.

This does NOT auto-deploy. Review the output (especially anything flagged
NEEDS VERIFICATION or NEEDS CLASSIFICATION), paste it into data/linkedin.py,
then follow the Deploy steps in CLAUDE.md.
"""
import ast
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from linkedin_countries import CLASSIFY, EXCLUDED, NORTH_CORE, SOUTH_CORE

REPO_ROOT = Path(__file__).parent.parent
LINKEDIN_PY = REPO_ROOT / "data" / "linkedin.py"


def load_csv(path):
    rows = {}
    with open(path, encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            rows[r["Company name"].strip()] = r
    return rows


def load_current(list_names=("NORTH", "SOUTH")):
    """Load company->dict lookup from the given lists in the currently
    committed data/linkedin.py, for lead-preservation and is_new diffing.
    Must scope this to the same list(s) you're regenerating — e.g. NA has
    its own companies that can share a name with an EMEA entry (same brand,
    different regional entity), and leads belong to one specific entity, not
    the company name in general."""
    src = LINKEDIN_PY.read_text()
    tree = ast.parse(src)
    ns = {}
    exec(compile(tree, "linkedin.py", "exec"), ns)
    current = {}
    for name in list_names:
        for d in ns[name]:
            current[d["co"].strip().lower()] = d
    return current


def merge(channels):
    """channels: list of (channel_name, csv_path) tuples, in the order given
    on the command line. views/clicks are summed across every channel that
    reports impressions; engagement is summed across all channels."""
    loaded = [(name, load_csv(path)) for name, path in channels]
    names = set()
    for _, rows in loaded:
        names |= set(rows)

    merged = []
    for co in names:
        if co in EXCLUDED:
            continue
        ch = []
        total_views = total_clicks = total_engagement = 0
        has_impressions = False
        for channel_name, rows in loaded:
            row = rows.get(co)
            if not row:
                continue
            imp = row["Paid impressions"].strip()
            clk = row["Paid clicks"].strip()
            eng = row["Paid engagements"].strip()
            present = False
            if imp:
                has_impressions = True
                present = True
                total_views += int(imp)
                total_clicks += int(clk) if clk else 0
            if eng:
                present = True
                total_engagement += int(eng)
            if present:
                ch.append(channel_name)
        if not ch:
            continue
        views = total_views if has_impressions else None
        clicks = total_clicks if has_impressions else None
        ctr = round(total_clicks / total_views * 100, 2) if has_impressions and total_views else None
        merged.append(dict(co=co, ch=ch, views=views, clicks=clicks, ctr=ctr, engagement=total_engagement))
    return merged


def classify(merged):
    classified, unclassified = [], []
    for d in merged:
        if d["co"] not in CLASSIFY:
            unclassified.append(d["co"])
            continue
        country, confidence = CLASSIFY[d["co"]]
        if country in NORTH_CORE:
            region = "NORTH"
        elif country in SOUTH_CORE:
            region = "SOUTH"
        else:
            unclassified.append(f'{d["co"]} (country "{country}" not in NORTH_CORE/SOUTH_CORE)')
            continue
        d["ctry"], d["region"], d["confidence"] = country, region, confidence
        classified.append(d)
    return classified, unclassified


def apply_threshold_and_leads(rows, current, views_threshold=150, engagement_threshold=15):
    """Inclusion rule:
    - Company has Ads views data: keep if views >= views_threshold. Clicks are
      not separately gated — whatever the real click count is, it's fine.
    - Company has NO Ads views (InMail-only): keep if engagement >=
      engagement_threshold, since engagement is the only signal available.
    - A lead always overrides both — a submitted lead is real signal
      regardless of views/engagement."""
    kept = []
    for d in rows:
        prior = current.get(d["co"].lower())
        lead, ltitle, ldate = (prior["lead"], prior["ltitle"], prior["ldate"]) if prior else (None, None, None)
        has_views = d["views"] is not None
        qualifies = (d["views"] >= views_threshold) if has_views else (d["engagement"] >= engagement_threshold)
        if qualifies or lead is not None:
            d["lead"], d["ltitle"], d["ldate"] = lead, ltitle, ldate
            d["is_new"] = prior is None
            kept.append(d)
    return kept


def fmt(rows_):
    out = []
    for d in sorted(rows_, key=lambda x: (x["views"] or 0), reverse=True):
        chs = ",".join(f'"{c}"' for c in d["ch"])
        views = d["views"] if d["views"] is not None else "None"
        clicks = d["clicks"] if d["clicks"] is not None else "None"
        ctr = d["ctr"] if d["ctr"] is not None else "None"
        lead = f'"{d["lead"]}"' if d["lead"] else "None"
        ltitle = f'"{d["ltitle"]}"' if d["ltitle"] else "None"
        ldate = f'"{d["ldate"]}"' if d["ldate"] else "None"
        is_new = ", is_new=True" if d["is_new"] else ""
        conf = "  # NEEDS VERIFICATION: EMEA base guessed" if d.get("confidence") == "M" else ""
        out.append(f'    dict(co="{d["co"]}", ctry="{d["ctry"]}", ch=[{chs}], views={views}, clicks={clicks}, '
                    f'ctr={ctr}, engagement={d["engagement"]}, lead={lead},ltitle={ltitle},ldate={ldate}{is_new}),{conf}')
    return "\n".join(out)


def main():
    args = sys.argv[1:]
    views_threshold = 150
    engagement_threshold = 15
    if "--views-threshold" in args:
        i = args.index("--views-threshold")
        views_threshold = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    if "--engagement-threshold" in args:
        i = args.index("--engagement-threshold")
        engagement_threshold = int(args[i + 1])
        args = args[:i] + args[i + 2:]

    channels = []
    for arg in args:
        if "=" not in arg:
            print(f"Expected Name=path.csv, got: {arg}\n")
            print(__doc__)
            sys.exit(1)
        name, path = arg.split("=", 1)
        channels.append((name, path))

    if not channels:
        print(__doc__)
        sys.exit(1)

    current = load_current()
    merged = merge(channels)
    classified, unclassified = classify(merged)
    kept = apply_threshold_and_leads(classified, current, views_threshold, engagement_threshold)

    north = [d for d in kept if d["region"] == "NORTH"]
    south = [d for d in kept if d["region"] == "SOUTH"]

    if unclassified:
        print(f"NEEDS CLASSIFICATION ({len(unclassified)}) — add to scripts/linkedin_countries.py and re-run:")
        for name in sorted(set(unclassified)):
            print(f"  - {name}")
        print()

    print(f"NORTH = [  # {len(north)} companies, {sum(1 for d in north if d['is_new'])} new")
    print(fmt(north))
    print("]\n")
    print(f"SOUTH = [  # {len(south)} companies, {sum(1 for d in south if d['is_new'])} new")
    print(fmt(south))
    print("]")


if __name__ == "__main__":
    main()
