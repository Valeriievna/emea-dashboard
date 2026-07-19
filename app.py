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
  .block-container { padding-top: 3rem; padding-bottom: 2rem; max-width: 1100px; }

  /* Page title */
  .dash-title { font-size: 22px; font-weight: 800; color: #fff; margin-bottom: 2px; padding-top: 8px; }
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
  .t-doc     { background:#111827; color:#4b7fa8; }
  .t-video   { background:#111827; color:#6b5a8a; }
  .t-article { background:#111827; color:#7a5a3a; }

  .num { color: #e5e7eb; font-variant-numeric: tabular-nums; }
  .dim { color: #374151; }

  .ctr-hi  { color: #4ade80; font-weight: 700; }
  .ctr-mid { color: #facc15; font-weight: 600; }
  .ctr-lo  { color: #6b7280; }

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
from data.linkedin import NORTH, SOUTH, UNIFY_NORTH, UNIFY_SOUTH
from data.g2 import G2_NORTH, G2_SOUTH

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

def fmt_channels(ch):
    return f'<span style="font-size:12px;color:#4b5563;">{len(ch)}</span>'

def fmt_engagement(v):
    if v is None or v < 15: return '<span class="dim">—</span>'
    return f'<span class="num">{v:,}</span>'

def fmt_lead(name, title, date):
    if name is None:
        return '<span class="no-lead">—</span>'
    date_part = f' &nbsp;<span class="lead-sub">· {date}</span>' if date else ''
    return f'<span class="lead-name">{name}</span><br><span class="lead-sub">{title}</span>{date_part}'

def render_table(data):
    rows = ""
    for d in data:
        has_lead = d["lead"] is not None
        cls = "lead-row" if has_lead else ""
        sv = lambda x: str(x) if x is not None else "-999"
        rows += f"""
        <tr class="{cls}">
          <td data-v="{d['co'].lower()}"><div class="co">{d['co']}{'<span style="background:#7c3aed;color:#e9d5ff;font-size:8px;font-weight:700;padding:1px 6px;border-radius:2px;margin-left:6px;vertical-align:middle;letter-spacing:0.5px;">NEW</span>' if d.get('is_new') else ''}</div><div class="ctry">{d['ctry']}</div></td>
          <td class="r" data-v="{sv(d['views'])}">{fmt_views(d['views'])}</td>
          <td class="r" data-v="{sv(d.get('engagement'))}">{fmt_engagement(d.get('engagement'))}</td>
          <td class="r" data-v="{sv(d['clicks'])}">{fmt_clicks(d['clicks'])}</td>
          <td class="r" data-v="{sv(d['ctr'])}">{fmt_ctr(d['ctr'])}</td>
          <td data-v="{'1' if has_lead else '0'}">{fmt_lead(d['lead'], d['ltitle'], d['ldate'])}</td>
          <td class="r" data-v="{len(d['ch'])}">{fmt_channels(d['ch'])}</td>
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
.t-doc{{background:#111827;color:#4b7fa8}}
.t-video{{background:#111827;color:#6b5a8a}}
.t-article{{background:#111827;color:#7a5a3a}}
.num{{color:#e5e7eb;font-variant-numeric:tabular-nums}}
.dim{{color:#374151}}
.ctr-hi{{color:#4ade80;font-weight:700}}
.ctr-mid{{color:#facc15;font-weight:600}}
.ctr-lo{{color:#6b7280}}
.lead-name{{font-weight:700;color:#fde68a;font-size:12px}}
.lead-sub{{font-size:10px;color:#92400e}}
.no-lead{{color:#1f2937}}
</style></head><body>
<table id="t">
  <thead><tr>
    <th data-col="0">COMPANY <span class="si">↕</span></th>
    <th class="r" data-col="1">AD VIEWS <span class="si">↕</span></th>
    <th class="r" data-col="2">ENGAGEMENT <span class="si">↕</span></th>
    <th class="r" data-col="3">AD CLICKS <span class="si">↕</span></th>
    <th class="r" data-col="4">CTR <span class="si">↕</span></th>
    <th data-col="5">LEAD SUBMITTED <span class="si">↕</span></th>
    <th class="r" data-col="6">TOUCHPOINTS <span class="si">↕</span></th>
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

def render_g2_table(data):
    act_order = {"High": 3, "Medium": 2, "Low": 1}
    act_style = {
        "High":   ("background:#14532d;color:#4ade80;", "High"),
        "Medium": ("background:#713f12;color:#facc15;", "Medium"),
        "Low":    ("background:#1c1c1c;color:#6b7280;",  "Low"),
    }
    dot_color = {"profile": "#60a5fa", "category": "#4b5563", "compare": "#f97316", "alt": "#fbbf24"}

    def build_detail(det):
        info = ""
        if det.get("website"):
            info += f'<div class="ir"><span class="il">Website</span><span class="iv lk">{det["website"]}</span></div>'
        if det.get("hq_full"):
            info += f'<div class="ir"><span class="il">HQ Location</span><span class="iv">{det["hq_full"]}</span></div>'
        if det.get("founded"):
            info += f'<div class="ir"><span class="il">Year Founded</span><span class="iv">{det["founded"]}</span></div>'
        if det.get("revenue"):
            info += f'<div class="ir"><span class="il">Annual Revenue</span><span class="iv">{det["revenue"]}</span></div>'
        if det.get("employees"):
            info += f'<div class="ir"><span class="il">Employee Count</span><span class="iv">{det["employees"]}</span></div>'

        feed = ""
        for item in det.get("feed", []):
            dc = dot_color.get(item["type"], "#4b5563")
            meta_parts = [p for p in [item.get("time"), item.get("loc")] if p]
            meta = f'<div class="fm">{"&nbsp;•&nbsp;".join(meta_parts)}</div>' if meta_parts else ""
            feed += f'<div class="fi"><span class="dot" style="background:{dc}"></span><div><div class="ft">{item["text"]}</div>{meta}</div></div>'
        if not feed:
            feed = '<div style="color:#374151;font-size:11px;font-style:italic;">Activity feed not yet available for this company.</div>'

        return f"""<div class="det">
  <div class="dc"><div class="dh">COMPANY INFO</div>{info}</div>
  <div class="dc"><div class="dh">ACTIVITY FEED</div><div class="fscroll">{feed}</div></div>
</div>"""

    rows = ""
    for i, d in enumerate(data):
        det    = d.get("details")
        sig    = d["signals"]  if d["signals"]  is not None else -999
        vis    = d["visitors"] if d["visitors"] is not None else -999
        act_n  = act_order[d["activity"]]
        sty, lbl = act_style[d["activity"]]
        act_html = f'<span style="{sty}font-size:9px;font-weight:700;padding:2px 9px;border-radius:3px;">{lbl}</span>'
        sig_html = f'<span class="num">{d["signals"]}</span>'  if d["signals"]  is not None else '<span class="dim">—</span>'
        vis_html = f'<span class="num">{d["visitors"]}</span>' if d["visitors"] is not None else '<span class="dim">—</span>'

        if det is not None:
            chev = f'<span class="chev" id="c{i}">&#9654;</span> '
            row_attr = f'class="xr" onclick="tog({i})" data-det="d{i}"'
        else:
            chev = ""
            row_attr = ""

        rows += f"""
        <tr {row_attr}>
          <td data-v="{d['co'].lower()}">{chev}<span class="co">{d['co']}</span><div class="ctry">{d['ctry']}</div></td>
          <td data-v="{act_n}">{act_html}</td>
          <td data-v="{d['visitor'].lower()}" style="color:#9ca3af;font-size:12px;">{d['visitor']}</td>
          <td data-v="{d['days']}" style="color:#6b7280;font-size:11px;">{d['last']}</td>
          <td class="r" data-v="{vis}">{vis_html}</td>
          <td class="r" data-v="{sig}">{sig_html}</td>
        </tr>"""

        if det is not None:
            rows += f"""
        <tr id="d{i}" class="det-row" style="display:none;">
          <td colspan="6" style="padding:0;">{build_detail(det)}</td>
        </tr>"""

    has_feed = any(d.get("details", {}) and d.get("details", {}).get("feed") for d in data)
    height   = 55 + len(data) * 50 + 20 + (420 if has_feed else 200 if any(d.get("details") for d in data) else 0)

    html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0d0d0d;font-family:'Segoe UI',Arial,sans-serif}}
table{{width:100%;border-collapse:collapse;font-size:12px}}
thead th{{text-align:left;padding:7px 12px;font-size:10px;font-weight:700;letter-spacing:.8px;
  color:#6b7280;border-bottom:2px solid #1e1e2e;white-space:nowrap;cursor:pointer;user-select:none}}
thead th:hover{{color:#a78bfa}}
thead th.r{{text-align:right}}
thead th .si{{margin-left:4px;font-size:9px;opacity:.4}}
thead th.asc .si,thead th.desc .si{{opacity:1;color:#a78bfa}}
tbody tr{{border-bottom:1px solid #111827}}
tbody tr.xr{{cursor:pointer}}
tbody tr.xr:hover td:first-child .co{{color:#c4b5fd}}
td{{padding:7px 12px;vertical-align:middle}}
td.r{{text-align:right}}
.co{{font-weight:600;color:#fff;font-size:13px;transition:color .15s}}
.ctry{{font-size:10px;color:#4b5563}}
.num{{color:#e5e7eb;font-variant-numeric:tabular-nums}}
.dim{{color:#374151}}
.chev{{color:#a78bfa;font-size:9px;margin-right:4px;display:inline-block;transition:transform .2s;}}
.chev.open{{transform:rotate(90deg)}}
/* Detail panel */
.det{{display:grid;grid-template-columns:230px 1fr;gap:0;background:#07070f;border-top:2px solid #1e1e2e;border-bottom:2px solid #1e1e2e;}}
.dc{{padding:18px 20px 20px;}}
.dc+.dc{{border-left:1px solid #1a1a2e;}}
.dh{{font-size:9px;font-weight:700;letter-spacing:1.5px;color:#4b5563;margin-bottom:14px;}}
.ir{{display:flex;flex-direction:column;margin-bottom:10px;}}
.il{{font-size:9px;color:#374151;letter-spacing:.4px;text-transform:uppercase;}}
.iv{{font-size:12px;color:#d1d5db;margin-top:2px;}}
.iv.lk{{color:#a78bfa;}}
.fscroll{{max-height:260px;overflow-y:auto;padding-right:4px;}}
.fi{{display:flex;gap:10px;margin-bottom:12px;align-items:flex-start;}}
.dot{{width:7px;height:7px;border-radius:50%;margin-top:5px;flex-shrink:0;}}
.ft{{font-size:12px;color:#d1d5db;line-height:1.45;}}
.fm{{font-size:10px;color:#4b5563;margin-top:3px;}}
</style></head><body>
<table id="g2t">
  <thead><tr>
    <th data-col="0">COMPANY <span class="si">↕</span></th>
    <th data-col="1">ACTIVITY <span class="si">↕</span></th>
    <th data-col="2">VISITOR LOCATION <span class="si">↕</span></th>
    <th data-col="3">LAST ACTIVE <span class="si">↕</span></th>
    <th class="r" data-col="4">VISITORS <span class="si">↕</span></th>
    <th class="r" data-col="5">SIGNALS <span class="si">↕</span></th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>
<script>
function tog(i) {{
  var det=document.getElementById('d'+i), chev=document.getElementById('c'+i);
  if(!det) return;
  var open=det.style.display!=='none';
  det.style.display=open?'none':'table-row';
  if(chev) chev.classList.toggle('open',!open);
}}
var cur=-1,asc=true;
document.querySelectorAll('#g2t thead th[data-col]').forEach(function(th){{
  th.addEventListener('click',function(){{
    var col=parseInt(th.getAttribute('data-col'));
    if(cur===col){{asc=!asc}}else{{cur=col;asc=(col===0||col===2)}}
    document.querySelectorAll('#g2t thead th').forEach(function(t){{
      t.classList.remove('asc','desc');
      var s=t.querySelector('.si');if(s)s.textContent='↕';
    }});
    th.classList.add(asc?'asc':'desc');
    th.querySelector('.si').textContent=asc?'↑':'↓';
    var tb=document.querySelector('#g2t tbody');
    var main=Array.from(tb.rows).filter(function(r){{return !r.classList.contains('det-row')}});
    main.sort(function(a,b){{
      var av=a.cells[col]?a.cells[col].getAttribute('data-v'):'';
      var bv=b.cells[col]?b.cells[col].getAttribute('data-v'):'';
      var an=parseFloat(av),bn=parseFloat(bv);
      if(!isNaN(an)&&!isNaN(bn))return asc?an-bn:bn-an;
      return asc?(av||'').localeCompare(bv||''):(bv||'').localeCompare(av||'');
    }});
    main.forEach(function(r){{
      tb.appendChild(r);
      var did=r.getAttribute('data-det');
      if(did){{var dr=document.getElementById(did);if(dr)tb.appendChild(dr);}}
    }});
  }});
}});
</script>
</body></html>"""
    components.html(html, height=height, scrolling=True)

# ── UI ───────────────────────────────────────────────────────────────────────

st.markdown('<div class="dash-title">EMEA Intent Dashboard</div>', unsafe_allow_html=True)

# ── Navigation ────────────────────────────────────────────────────────────────
tab_li, tab_g2 = st.tabs(["LinkedIn Intent", "G2 Intent"])

# ── LinkedIn Intent tab ───────────────────────────────────────────────────────
with tab_li:
    col_campaign, col_region, _ = st.columns([2, 2, 2])
    with col_campaign:
        st.caption("CAMPAIGN")
        campaign = st.radio("Campaign", ["Smart Tests", "Unify (AI Governance)"],
                            horizontal=False, label_visibility="collapsed")
    with col_region:
        st.caption("REGION")
        region = st.radio("Region", ["EMEA North", "EMEA South"],
                          horizontal=False, label_visibility="collapsed")

    st.divider()

    if campaign == "Smart Tests":
        data = NORTH if region == "EMEA North" else SOUTH
        date_label = "Last 90 days (through Jul 18, 2026)"
    else:
        data = UNIFY_NORTH if region == "EMEA North" else UNIFY_SOUTH
        date_label = "Jul 1 – 12, 2026"

    flag = "UK · Germany · Netherlands · Sweden · Switzerland · Ireland" if region == "EMEA North" else "France · UAE · Saudi Arabia · Israel · Spain"

    st.markdown(f'<div class="section-lbl">{region.upper()} — {flag}</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:13px; font-weight:700; color:#a78bfa; letter-spacing:0.5px; margin-bottom:10px;">{date_label}</div>', unsafe_allow_html=True)
    st.markdown("""
<div style="font-size:11px; color:#6b7280; background:#111827; border-left:2px solid #a78bfa;
            padding:8px 14px; margin-bottom:14px; border-radius:0 4px 4px 0; line-height:1.6;">
  <b style="color:#d1d5db;">CTR</b> (Click-Through Rate) — the % of people who saw the ad and clicked it.
  &nbsp;<span style="color:#4ade80;">■</span> ≥2% strong
  &nbsp;<span style="color:#facc15;">■</span> ≥1% good
  &nbsp;<span style="color:#6b7280;">■</span> &lt;1% low
  <br><b style="color:#d1d5db;">Engagement</b> = all interactions incl. clicks &nbsp;·&nbsp;
  <b style="color:#d1d5db;">Ad Clicks</b> = clicks only &nbsp;·&nbsp;
  <b style="color:#d1d5db;">Touchpoints</b> = # of ad types/channels seen
</div>
""", unsafe_allow_html=True)
    render_table(data)

# ── G2 Intent tab ─────────────────────────────────────────────────────────────
with tab_g2:
    col_region_g2, _, _ = st.columns([2, 2, 2])
    with col_region_g2:
        st.caption("REGION")
        region_g2 = st.radio("Region G2", ["EMEA North", "EMEA South"],
                             horizontal=False, label_visibility="collapsed")

    st.divider()

    g2_data = G2_NORTH if region_g2 == "EMEA North" else G2_SOUTH
    flag_g2 = "UK · Germany · Netherlands · Sweden · Switzerland · Ireland" if region_g2 == "EMEA North" else "France · UAE · Saudi Arabia · Israel · Spain"

    st.markdown(f'<div class="section-lbl">{region_g2.upper()} — {flag_g2}</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:13px; font-weight:700; color:#a78bfa; letter-spacing:0.5px; margin-bottom:4px;">G2 Intent · Last 90 days</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px; color:#6b7280; margin-bottom:10px;">Updated Jul 13, 2026</div>', unsafe_allow_html=True)
    render_g2_table(g2_data)

