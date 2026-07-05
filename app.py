import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="EMEA Intent — Sales",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }

  /* Page title */
  .dash-title { font-size: 22px; font-weight: 800; color: #fff; margin-bottom: 2px; }
  .dash-sub   { font-size: 12px; color: #6b7280; margin-bottom: 24px; }

  /* Table */
  table { width: 100%; border-collapse: collapse; font-size: 12px; }
  thead th {
    text-align: left; padding: 7px 12px;
    font-size: 10px; font-weight: 700; letter-spacing: 0.8px;
    color: #6b7280; border-bottom: 2px solid #1e1e2e; white-space: nowrap;
  }
  thead th.r { text-align: right; }
  tbody tr { border-bottom: 1px solid #111827; }
  tbody tr:hover { background: #111827; }
  tbody tr.lead-row { background: #1a1500; }
  tbody tr.lead-row:hover { background: #231d00; }
  td { padding: 7px 12px; vertical-align: middle; }
  td.r { text-align: right; }

  .co  { font-weight: 600; color: #fff; font-size: 13px; }
  .ctry { font-size: 10px; color: #4b5563; }

  .tags { display: flex; gap: 4px; flex-wrap: wrap; }
  .tag  { font-size: 9px; font-weight: 700; padding: 2px 7px; border-radius: 3px; white-space: nowrap; }
  .t-ads     { background:#312e81; color:#a5b4fc; }
  .t-inmail  { background:#14532d; color:#86efac; }
  .t-demo    { background:#451a03; color:#fdba74; }

  .num { color: #e5e7eb; font-variant-numeric: tabular-nums; }
  .dim { color: #374151; }

  .ctr-hi  { color: #4ade80; font-weight: 700; }
  .ctr-mid { color: #facc15; font-weight: 600; }
  .ctr-lo  { color: #6b7280; }

  .op-hi  { color: #4ade80; font-weight: 700; }
  .op-mid { color: #facc15; font-weight: 600; }
  .op-lo  { color: #6b7280; }

  .lead-name { font-weight: 700; color: #fde68a; font-size: 12px; }
  .lead-sub  { font-size: 10px; color: #92400e; }
  .no-lead   { color: #1f2937; }

  /* Section label */
  .section-lbl {
    font-size: 10px; font-weight: 700; letter-spacing: 2px;
    color: #a78bfa; margin: 20px 0 8px;
    border-bottom: 1px solid #2a2a3a; padding-bottom: 4px;
  }

  /* G2 placeholder */
  .g2-placeholder {
    border: 2px dashed #2a2a3a; border-radius: 8px;
    padding: 60px 40px; text-align: center; margin-top: 20px;
  }
  .g2-placeholder h3 { color: #4b5563; font-size: 16px; margin-bottom: 8px; }
  .g2-placeholder p  { color: #374151; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────

NORTH = [
    # ── leads first ──
    dict(co="Sky",                    ctry="UK",            ch=["Ads","InMail"],        views=774,   clicks=22,   ctr=2.84, op=46.02, lead="Megha Parameswaran",   ltitle="Software Engineer",        ldate="Apr 16"),
    dict(co="Delivery Hero",          ctry="Germany",       ch=["Ads"],                 views=651,   clicks=16,   ctr=2.46, op=None,  lead="Kanchan Khatri",       ltitle="Engineering Manager",      ldate="Mar 13"),
    dict(co="Ericsson",               ctry="Sweden",        ch=["InMail"],              views=None,  clicks=None, ctr=None, op=55.71, lead="Jitender Thakur",      ltitle="Senior Engineer",          ldate="Mar 12"),
    dict(co="Siemens Healthineers",   ctry="Germany",       ch=["InMail"],              views=None,  clicks=None, ctr=None, op=50.91, lead="Rithika Ravichandran",  ltitle="AI/ML Engineer",           ldate="Apr 19"),
    # ── no lead ──
    dict(co="IBM",                    ctry="UK",            ch=["Ads","Demo","InMail"], views=3145,  clicks=28,   ctr=0.89, op=51.56, lead=None,ltitle=None,ldate=None),
    dict(co="Lloyds Banking Group",   ctry="UK",            ch=["Ads","InMail"],        views=1331,  clicks=26,   ctr=1.95, op=41.13, lead=None,ltitle=None,ldate=None),
    dict(co="Tata Consultancy Svcs",  ctry="UK",            ch=["Ads"],                 views=1187,  clicks=18,   ctr=1.52, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Nagarro",                ctry="Germany",       ch=["Ads","Demo","InMail"], views=1337,  clicks=16,   ctr=1.20, op=56.25, lead=None,ltitle=None,ldate=None),
    dict(co="Cognizant",              ctry="UK",            ch=["Ads"],                 views=717,   clicks=15,   ctr=2.09, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Arm",                    ctry="UK",            ch=["Ads","Demo","InMail"], views=1055,  clicks=13,   ctr=1.23, op=55.42, lead=None,ltitle=None,ldate=None),
    dict(co="Swisscom",               ctry="Switzerland",   ch=["Ads"],                 views=1070,  clicks=12,   ctr=1.12, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Amazon Web Services",    ctry="Ireland",       ch=["Ads"],                 views=1085,  clicks=10,   ctr=0.92, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Mercedes-Benz AG",       ctry="Germany",       ch=["Ads"],                 views=259,   clicks=5,    ctr=1.93, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Volvo Cars",             ctry="Sweden",        ch=["Ads","Demo","InMail"], views=706,   clicks=3,    ctr=0.42, op=75.00, lead=None,ltitle=None,ldate=None),
]

SOUTH = [
    # ── leads first ──
    dict(co="Qualitest",                   ctry="Israel",        ch=["Ads","Demo","InMail"], views=1545, clicks=26,   ctr=1.68, op=56.00, lead="Zumirrah Khalid",   ltitle="SDET",                     ldate="Apr 17"),
    dict(co="stc",                         ctry="Saudi Arabia",  ch=["Ads","Demo"],          views=1212, clicks=14,   ctr=1.16, op=None,  lead="Jamal Saleh",       ltitle="QA and Test Lead",         ldate="Mar 10"),
    dict(co="Expleo Group",                ctry="France",        ch=["Ads","Demo"],          views=1551, clicks=15,   ctr=0.97, op=None,  lead="Sherin Elmoghazy",  ltitle="Sr QA Analyst",            ldate="Mar 6"),
    dict(co="Technology Innovation Inst.", ctry="UAE",           ch=["InMail"],              views=None, clicks=None, ctr=None, op=None,  lead="Shaaban Hassan",    ltitle="Senior Software Engineer", ldate="Jun 24"),
    dict(co="SEAT, S.A.",                  ctry="Spain",         ch=["InMail"],              views=None, clicks=None, ctr=None, op=None,  lead="Xavier Agustin",    ltitle="Manager Vehicle Testing",  ldate="Apr 15"),
    # ── no lead ──
    dict(co="Capgemini",       ctry="France",        ch=["Ads","Demo","InMail"], views=5727, clicks=66,   ctr=1.15, op=66.06, lead=None,ltitle=None,ldate=None),
    dict(co="Emirates NBD",    ctry="UAE",           ch=["Ads","Demo","InMail"], views=2506, clicks=49,   ctr=1.96, op=68.35, lead=None,ltitle=None,ldate=None),
    dict(co="Emirates",        ctry="UAE",           ch=["Ads","Demo","InMail"], views=3130, clicks=47,   ctr=1.50, op=46.25, lead=None,ltitle=None,ldate=None),
    dict(co="Elm Company",     ctry="Saudi Arabia",  ch=["Ads","Demo","InMail"], views=3378, clicks=42,   ctr=1.24, op=58.21, lead=None,ltitle=None,ldate=None),
    dict(co="Sopra Steria",    ctry="France",        ch=["Ads","Demo","InMail"], views=1648, clicks=22,   ctr=1.33, op=49.02, lead=None,ltitle=None,ldate=None),
    dict(co="ALTEN",           ctry="France",        ch=["Ads","Demo"],          views=1102, clicks=16,   ctr=1.45, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Indra Group",     ctry="Spain",         ch=["Ads","Demo"],          views=1336, clicks=15,   ctr=1.12, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="EJADA",           ctry="Saudi Arabia",  ch=["Ads","Demo"],          views=1332, clicks=11,   ctr=0.83, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Thales",          ctry="France",        ch=["Ads","Demo"],          views=1265, clicks=10,   ctr=0.79, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Mobileye",        ctry="Israel",        ch=["Ads","Demo"],          views=590,  clicks=4,    ctr=0.68, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="hiberus",         ctry="Spain",         ch=["Ads","Demo"],          views=1193, clicks=3,    ctr=0.25, op=None,  lead=None,ltitle=None,ldate=None),
]

# ── Helpers ───────────────────────────────────────────────────────────────────

def fmt_views(v):
    if v is None: return '<span class="dim">—</span>'
    return f'<span class="num">{v:,}</span>'

def fmt_clicks(v):
    if v is None: return '<span class="dim">—</span>'
    return f'<span class="num">{v}</span>'

def fmt_ctr(v):
    if v is None: return '<span class="dim">—</span>'
    if v >= 2:    return f'<span class="ctr-hi">{v:.2f}%</span>'
    if v >= 1:    return f'<span class="ctr-mid">{v:.2f}%</span>'
    return         f'<span class="ctr-lo">{v:.2f}%</span>'

def fmt_open(v, has_clicks, inmail_only=False):
    if v is None: return '<span class="dim">—</span>'
    if not has_clicks and not inmail_only: return '<span class="dim">—</span>'
    if v >= 55:   return f'<span class="op-hi">{v:.2f}%</span>'
    if v >= 40:   return f'<span class="op-mid">{v:.2f}%</span>'
    return         f'<span class="op-lo">{v:.2f}%</span>'

def fmt_channels(ch):
    tag_map = {"Ads": "t-ads", "InMail": "t-inmail", "Demo": "t-demo"}
    pills = "".join(f'<span class="tag {tag_map[c]}">{c}</span>' for c in ch)
    return f'<div class="tags">{pills}</div>'

def fmt_lead(name, title, date):
    if name is None:
        return '<span class="no-lead">—</span>'
    return f'<span class="lead-name">{name}</span><br><span class="lead-sub">{title}</span>'

def render_table(data):
    rows = ""
    for d in data:
        has_lead = d["lead"] is not None
        has_clicks = d["clicks"] is not None
        inmail_only = d["views"] is None
        cls = "lead-row" if has_lead else ""
        sv = lambda x: str(x) if x is not None else "-999"
        rows += f"""
        <tr class="{cls}">
          <td data-v="{d['co'].lower()}"><div class="co">{d['co']}</div><div class="ctry">{d['ctry']}</div></td>
          <td>{fmt_channels(d['ch'])}</td>
          <td class="r" data-v="{sv(d['views'])}">{fmt_views(d['views'])}</td>
          <td class="r" data-v="{sv(d['clicks'])}">{fmt_clicks(d['clicks'])}</td>
          <td class="r" data-v="{sv(d['ctr'])}">{fmt_ctr(d['ctr'])}</td>
          <td class="r" data-v="{sv(d['op'])}">{fmt_open(d['op'], has_clicks, inmail_only)}</td>
          <td data-v="{'1' if has_lead else '0'}">{fmt_lead(d['lead'], d['ltitle'], d['ldate'])}</td>
        </tr>"""

    height = 55 + len(data) * 52 + 20
    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0d0d0d;font-family:'Segoe UI',Arial,sans-serif}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
thead th{{text-align:left;padding:7px 12px;font-size:10px;font-weight:700;letter-spacing:.8px;
  color:#6b7280;border-bottom:2px solid #1e1e2e;white-space:nowrap;
  cursor:pointer;user-select:none}}
thead th:hover{{color:#a78bfa}}
thead th.r{{text-align:right}}
thead th .si{{margin-left:4px;font-size:9px;opacity:.4}}
thead th.asc .si{{opacity:1;color:#a78bfa}}
thead th.desc .si{{opacity:1;color:#a78bfa}}
tbody tr{{border-bottom:1px solid #111827}}
tbody tr:hover{{background:#111827}}
tbody tr.lead-row{{background:#1a1500}}
tbody tr.lead-row:hover{{background:#231d00}}
td{{padding:7px 12px;vertical-align:middle}}
td.r{{text-align:right}}
.co{{font-weight:600;color:#fff;font-size:13px}}
.ctry{{font-size:10px;color:#4b5563}}
.tags{{display:flex;gap:4px;flex-wrap:wrap}}
.tag{{font-size:9px;font-weight:700;padding:2px 7px;border-radius:3px;white-space:nowrap}}
.t-ads{{background:#312e81;color:#a5b4fc}}
.t-inmail{{background:#14532d;color:#86efac}}
.t-demo{{background:#451a03;color:#fdba74}}
.num{{color:#e5e7eb;font-variant-numeric:tabular-nums}}
.dim{{color:#374151}}
.ctr-hi{{color:#4ade80;font-weight:700}}
.ctr-mid{{color:#facc15;font-weight:600}}
.ctr-lo{{color:#6b7280}}
.op-hi{{color:#4ade80;font-weight:700}}
.op-mid{{color:#facc15;font-weight:600}}
.op-lo{{color:#6b7280}}
.lead-name{{font-weight:700;color:#fde68a;font-size:12px}}
.lead-sub{{font-size:10px;color:#92400e}}
.no-lead{{color:#1f2937}}
</style></head><body>
<table id="t">
  <thead><tr>
    <th data-col="0">COMPANY <span class="si">↕</span></th>
    <th>CHANNELS</th>
    <th class="r" data-col="2">AD VIEWS <span class="si">↕</span></th>
    <th class="r" data-col="3">AD CLICKS <span class="si">↕</span></th>
    <th class="r" data-col="4">CTR <span class="si">↕</span></th>
    <th class="r" data-col="5">INMAIL OPEN RATE <span class="si">↕</span></th>
    <th data-col="6">LEAD SUBMITTED <span class="si">↕</span></th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
<script>
var cur=-1,asc=true;
document.querySelectorAll('thead th[data-col]').forEach(function(th){{
  th.addEventListener('click',function(){{
    var col=parseInt(th.getAttribute('data-col'));
    if(cur===col){{asc=!asc}}else{{cur=col;asc=col===0}}
    document.querySelectorAll('thead th').forEach(function(t){{
      t.classList.remove('asc','desc');
      var s=t.querySelector('.si');if(s)s.textContent='↕';
    }});
    th.classList.add(asc?'asc':'desc');
    th.querySelector('.si').textContent=asc?'↑':'↓';
    var tb=document.querySelector('#t tbody');
    Array.from(tb.rows).sort(function(a,b){{
      var av=a.cells[col].getAttribute('data-v');
      var bv=b.cells[col].getAttribute('data-v');
      var an=parseFloat(av),bn=parseFloat(bv);
      if(!isNaN(an)&&!isNaN(bn))return asc?an-bn:bn-an;
      return asc?av.localeCompare(bv):bv.localeCompare(av);
    }}).forEach(function(r){{tb.appendChild(r)}});
  }});
}});
</script>
</body></html>"""
    components.html(html, height=height, scrolling=False)

# ── UI ───────────────────────────────────────────────────────────────────────

st.markdown('<div class="dash-title">EMEA Intent Dashboard</div>', unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
col_campaign, col_region, col_data = st.columns([2, 2, 2])
with col_campaign:
    st.caption("CAMPAIGN")
    campaign = st.radio("Campaign", ["Smart Tests"],
                        horizontal=False, label_visibility="collapsed")
    st.markdown("""
    <div style="opacity:0.3; cursor:not-allowed; font-size:14px; padding:2px 0 0 2px; color:#fff;">
      ○ &nbsp;Unify (AI Governance)
      <span style="font-size:10px; color:#6b7280;"> — coming soon</span>
    </div>
    """, unsafe_allow_html=True)
with col_region:
    st.caption("REGION")
    region = st.radio("Region", ["EMEA North", "EMEA South"],
                      horizontal=False, label_visibility="collapsed")
with col_data:
    st.caption("DATA SOURCE")
    data_type = st.radio("Data source", ["LinkedIn Intent", "G2 Intent"],
                         horizontal=False, label_visibility="collapsed")

st.divider()

# ── Content ───────────────────────────────────────────────────────────────────

if False:
    st.markdown(f"""
    <div class="g2-placeholder">
      <h3>{campaign} — data coming soon</h3>
      <p>Intent data for this campaign will appear here once available.</p>
    </div>
    """, unsafe_allow_html=True)

elif data_type == "G2 Intent":
    st.markdown("""
    <div class="g2-placeholder">
      <h3>G2 Intent data coming soon</h3>
      <p>Paste G2 intent export here to see which accounts are actively researching on G2.</p>
    </div>
    """, unsafe_allow_html=True)

else:
    data = NORTH if region == "EMEA North" else SOUTH
    flag = "UK · Germany · Netherlands · Sweden · Switzerland · Ireland" if region == "EMEA North" else "France · UAE · Saudi Arabia · Israel · Spain"

    st.markdown(f'<div class="section-lbl">{region.upper()} — {flag}</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px; color:#4b5563; margin-bottom:8px;">Apr 1 – Jun 30, 2026</div>', unsafe_allow_html=True)
    render_table(data)

    leads = [d for d in data if d["lead"]]
    total_views = sum(d["views"] for d in data if d["views"])
    total_clicks = sum(d["clicks"] for d in data if d["clicks"])

    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Companies reached", len(data))
    c2.metric("Total ad views",    f"{total_views:,}")
    c3.metric("Total ad clicks",   total_clicks)
    c4.metric("Leads submitted",   len(leads))
