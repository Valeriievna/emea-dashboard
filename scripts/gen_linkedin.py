"""
Regenerate LinkedIn Smart Test NORTH/SOUTH from two Campaign Manager "companies"
exports (same window size, e.g. both 90-day): one for the Ads ad set, one for
the InMail ad set.

Usage:
    python3 scripts/gen_linkedin.py ads.csv inmail.csv [--threshold 15]

What it does:
    1. Merges the two exports by company name.
       - views/clicks/ctr come only from the Ads export (InMail has neither).
       - engagement = Ads Paid engagements + InMail Paid engagements.
    2. Classifies country/region using scripts/linkedin_countries.py (the
       running lookup). Companies not in that lookup are printed separately
       under NEEDS CLASSIFICATION — add them to linkedin_countries.py by hand
       (LinkedIn's export doesn't report company country) and re-run.
    3. Keeps a company if engagement >= threshold (default 15) OR it already
       has a lead in the currently committed data/linkedin.py.
    4. Computes is_new by diffing against the currently committed NORTH/SOUTH
       in data/linkedin.py. Only meaningful if the previous refresh used the
       SAME window size (30 vs 90-day totals aren't comparable).
    5. Preserves lead/ltitle/ldate from the currently committed data for any
       company that already has one (add new leads by hand afterward from the
       separate lead-gen export, since Campaign Manager's company export only
       gives lead counts, not identity).
    6. Prints ready-to-paste NORTH/SOUTH blocks to stdout.

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


def load_current():
    src = LINKEDIN_PY.read_text()
    tree = ast.parse(src)
    ns = {}
    exec(compile(tree, "linkedin.py", "exec"), ns)
    current = {}
    for d in ns["NORTH"] + ns["SOUTH"]:
        current[d["co"].strip().lower()] = d
    return current


def merge(ads_path, inmail_path):
    ads = load_csv(ads_path)
    inmail = load_csv(inmail_path)
    names = set(ads) | set(inmail)

    merged = []
    for name in names:
        if name in EXCLUDED:
            continue
        a = ads.get(name)
        m = inmail.get(name)
        ch, views, clicks, ctr = [], None, None, None
        ads_eng = inmail_eng = 0
        if a:
            imp, clk, eng = a["Paid impressions"].strip(), a["Paid clicks"].strip(), a["Paid engagements"].strip()
            if imp:
                ch.append("Ads")
                views = int(imp)
                clicks = int(clk) if clk else 0
                ctr = round(clicks / views * 100, 2) if views else None
            ads_eng = int(eng) if eng else 0
        if m:
            eng = m["Paid engagements"].strip()
            if eng:
                ch.append("InMail")
                inmail_eng = int(eng)
        if not ch:
            continue
        merged.append(dict(co=name, ch=ch, views=views, clicks=clicks, ctr=ctr,
                            engagement=ads_eng + inmail_eng))
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


def apply_threshold_and_leads(rows, current, threshold):
    kept = []
    for d in rows:
        prior = current.get(d["co"].lower())
        lead, ltitle, ldate = (prior["lead"], prior["ltitle"], prior["ldate"]) if prior else (None, None, None)
        if d["engagement"] >= threshold or lead is not None:
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
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    ads_path, inmail_path = sys.argv[1], sys.argv[2]
    threshold = 15
    if "--threshold" in sys.argv:
        threshold = int(sys.argv[sys.argv.index("--threshold") + 1])

    current = load_current()
    merged = merge(ads_path, inmail_path)
    classified, unclassified = classify(merged)
    kept = apply_threshold_and_leads(classified, current, threshold)

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
