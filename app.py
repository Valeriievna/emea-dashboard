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
    dict(co="Sky",                    ctry="UK",            ch=["Ads","InMail"],        views=774,   clicks=22,   ctr=2.84, op=55.17, lead="Megha Parameswaran",   ltitle="Software Engineer",        ldate="Apr 16"),
    dict(co="Delivery Hero",          ctry="Germany",       ch=["Ads","InMail"],        views=651,   clicks=16,   ctr=2.46, op=None,  lead="Kanchan Khatri",       ltitle="Engineering Manager",      ldate="Mar 13"),
    dict(co="Ericsson",               ctry="Sweden",        ch=["Ads","InMail"],        views=445,   clicks=4,    ctr=0.90, op=70.59, lead="Jitender Thakur",      ltitle="Senior Engineer",          ldate="Mar 12"),
    dict(co="Siemens Healthineers",   ctry="Germany",       ch=["InMail"],              views=None,  clicks=None, ctr=None, op=50.91, lead="Rithika Ravichandran",  ltitle="AI/ML Engineer",           ldate="Apr 19"),
    # ── no lead ──
    dict(co="IBM",                    ctry="UK",            ch=["Ads","Demo","InMail"], views=3145,  clicks=28,   ctr=0.89, op=51.56, lead=None,ltitle=None,ldate=None),
    dict(co="Lloyds Banking Group",   ctry="UK",            ch=["Ads","InMail"],        views=1548,  clicks=30,   ctr=1.94, op=41.13, lead=None,ltitle=None,ldate=None),
    dict(co="Tata Consultancy Svcs",  ctry="UK",            ch=["Ads"],                 views=1187,  clicks=18,   ctr=1.52, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Nagarro",                ctry="Germany",       ch=["Ads","Demo","InMail"], views=1337,  clicks=16,   ctr=1.20, op=56.25, lead=None,ltitle=None,ldate=None),
    dict(co="Arm",                    ctry="UK",            ch=["Ads","Demo","InMail"], views=1312,  clicks=19,   ctr=1.45, op=55.42, lead=None,ltitle=None,ldate=None),
    dict(co="Amazon Web Services",    ctry="Ireland",       ch=["Ads"],                 views=1085,  clicks=10,   ctr=0.92, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Swisscom",               ctry="Switzerland",   ch=["Ads"],                 views=1070,  clicks=12,   ctr=1.12, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Cognizant",              ctry="UK",            ch=["Ads","InMail"],        views=717,   clicks=15,   ctr=2.09, op=133.33,lead=None,ltitle=None,ldate=None),
    dict(co="Volvo Cars",             ctry="Sweden",        ch=["Ads","Demo","InMail"], views=706,   clicks=3,    ctr=0.42, op=75.00, lead=None,ltitle=None,ldate=None),
    dict(co="Siemens",                ctry="Germany",       ch=["Ads"],                 views=702,   clicks=9,    ctr=1.28, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="AUMOVIO",                ctry="Europe",        ch=["Ads"],                 views=670,   clicks=4,    ctr=0.60, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Deutsche Bank",          ctry="Germany",       ch=["Ads"],                 views=546,   clicks=5,    ctr=0.92, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Vodafone",               ctry="UK",            ch=["Ads"],                 views=545,   clicks=3,    ctr=0.55, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="SAP",                    ctry="Germany",       ch=["Ads"],                 views=496,   clicks=4,    ctr=0.81, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="LSEG",                   ctry="UK",            ch=["Ads"],                 views=415,   clicks=5,    ctr=1.20, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Rabobank",               ctry="Netherlands",   ch=["Ads"],                 views=336,   clicks=3,    ctr=0.89, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="ASML",                   ctry="Netherlands",   ch=["Ads"],                 views=331,   clicks=4,    ctr=1.21, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Bosch",                  ctry="Germany",       ch=["Ads"],                 views=331,   clicks=3,    ctr=0.91, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Nokia",                  ctry="Finland",       ch=["Ads"],                 views=314,   clicks=5,    ctr=1.59, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Mercedes-Benz AG",       ctry="Germany",       ch=["Ads"],                 views=259,   clicks=5,    ctr=1.93, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="IKEA",                   ctry="Sweden",        ch=["Ads"],                 views=231,   clicks=4,    ctr=1.73, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Wolt",                   ctry="Finland",       ch=["Ads"],                 views=229,   clicks=None, ctr=None, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="NXP Semiconductors",     ctry="Netherlands",   ch=["Ads"],                 views=218,   clicks=None, ctr=None, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Eaton",                  ctry="Ireland",       ch=["Ads"],                 views=210,   clicks=6,    ctr=2.86, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Continental",            ctry="Germany",       ch=["Ads"],                 views=209,   clicks=None, ctr=None, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Revolut",                ctry="UK",            ch=["Ads"],                 views=206,   clicks=None, ctr=None, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Fidelity Investments",   ctry="Ireland",       ch=["InMail"],              views=None,  clicks=None, ctr=None, op=66.67, lead=None,ltitle=None,ldate=None),
]

SOUTH = [
    # ── leads first ──
    dict(co="Qualitest",                   ctry="Israel",        ch=["Ads","Demo","InMail"], views=1545, clicks=26,   ctr=1.68, op=56.00, lead="Zumirrah Khalid",   ltitle="SDET",                     ldate="Apr 17"),
    dict(co="stc",                         ctry="Saudi Arabia",  ch=["Ads","Demo","InMail"], views=1212, clicks=14,   ctr=1.16, op=38.10, lead="Jamal Saleh",       ltitle="QA and Test Lead",         ldate="Mar 10"),
    dict(co="Expleo Group",                ctry="France",        ch=["Ads","Demo","InMail"], views=1551, clicks=15,   ctr=0.97, op=57.14, lead="Sherin Elmoghazy",  ltitle="Sr QA Analyst",            ldate="Mar 6"),
    dict(co="Technology Innovation Inst.", ctry="UAE",           ch=["InMail"],              views=None, clicks=None, ctr=None, op=120.00,lead="Shaaban Hassan",    ltitle="Senior Software Engineer", ldate="Jun 24"),
    dict(co="SEAT, S.A.",                  ctry="Spain",         ch=["InMail"],              views=None, clicks=None, ctr=None, op=None,  lead="Xavier Agustin",    ltitle="Manager Vehicle Testing",  ldate="Apr 15"),
    # ── no lead ──
    dict(co="Capgemini",       ctry="France",        ch=["Ads","Demo","InMail"], views=5727, clicks=66,   ctr=1.15, op=66.06, lead=None,ltitle=None,ldate=None),
    dict(co="Elm Company",     ctry="Saudi Arabia",  ch=["Ads","Demo","InMail"], views=3378, clicks=42,   ctr=1.24, op=58.21, lead=None,ltitle=None,ldate=None),
    dict(co="Emirates",        ctry="UAE",           ch=["Ads","Demo","InMail"], views=3130, clicks=47,   ctr=1.50, op=46.25, lead=None,ltitle=None,ldate=None),
    dict(co="Emirates NBD",    ctry="UAE",           ch=["Ads","Demo","InMail"], views=3577, clicks=67,   ctr=1.87, op=68.35, lead=None,ltitle=None,ldate=None),
    dict(co="Sopra Steria",    ctry="France",        ch=["Ads","Demo","InMail"], views=1648, clicks=22,   ctr=1.33, op=49.02, lead=None,ltitle=None,ldate=None),
    dict(co="ALTEN",           ctry="France",        ch=["Ads","Demo"],          views=1102, clicks=16,   ctr=1.45, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Indra Group",     ctry="Spain",         ch=["Ads","Demo"],          views=1336, clicks=15,   ctr=1.12, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="EJADA",           ctry="Saudi Arabia",  ch=["Ads","Demo"],          views=1332, clicks=11,   ctr=0.83, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Thales",          ctry="France",        ch=["Ads","Demo"],          views=1265, clicks=10,   ctr=0.79, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="hiberus",         ctry="Spain",         ch=["Ads","Demo"],          views=1193, clicks=3,    ctr=0.25, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Mobileye",        ctry="Israel",        ch=["Ads","Demo"],          views=590,  clicks=4,    ctr=0.68, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="ING Türkiye",     ctry="Turkey",        ch=["Ads"],                 views=473,  clicks=5,    ctr=1.06, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Akbank",          ctry="Turkey",        ch=["Ads"],                 views=447,  clicks=None, ctr=None, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="VakıfBank",       ctry="Turkey",        ch=["Ads"],                 views=371,  clicks=None, ctr=None, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Halkbank",        ctry="Turkey",        ch=["Ads"],                 views=319,  clicks=None, ctr=None, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Valeo",           ctry="France",        ch=["Ads"],                 views=254,  clicks=None, ctr=None, op=None,  lead=None,ltitle=None,ldate=None),
    dict(co="Sogeti",          ctry="France",        ch=["InMail"],              views=None, clicks=None, ctr=None, op=50.00, lead=None,ltitle=None,ldate=None),
]

UNIFY_NORTH = [
    # ch = which of the 3 Unify ad sets the company appeared in: Doc / Video / Article
    dict(co="SAP",                   ctry="Germany",     ch=["Doc","Video","Article"], views=807, clicks=26,   ctr=3.22, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Siemens",               ctry="Germany",     ch=["Doc","Video","Article"], views=622, clicks=8,    ctr=1.29, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Bosch",                 ctry="Germany",     ch=["Doc","Video","Article"], views=377, clicks=4,    ctr=1.06, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Volvo Cars",            ctry="Sweden",      ch=["Doc","Video","Article"], views=336, clicks=7,    ctr=2.08, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Ericsson",              ctry="Sweden",      ch=["Doc","Video","Article"], views=317, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="IKEA",                  ctry="Sweden",      ch=["Doc","Video","Article"], views=254, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="BASF",                  ctry="Germany",     ch=["Doc","Video","Article"], views=252, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Vodafone",              ctry="UK",          ch=["Doc","Video","Article"], views=248, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="AUMOVIO",               ctry="Europe",      ch=["Doc","Video","Article"], views=233, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Deutsche Bank",         ctry="Germany",     ch=["Doc","Video","Article"], views=219, clicks=3,    ctr=1.37, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Shell",                 ctry="Netherlands", ch=["Doc","Video","Article"], views=211, clicks=4,    ctr=1.90, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="UBS",                   ctry="Switzerland", ch=["Doc","Video","Article"], views=208, clicks=3,    ctr=1.44, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Nokia",                 ctry="Finland",     ch=["Doc","Video","Article"], views=187, clicks=6,    ctr=3.21, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Continental",           ctry="Germany",     ch=["Doc","Video","Article"], views=184, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Infineon Technologies", ctry="Germany",     ch=["Doc","Video","Article"], views=175, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Booking.com",           ctry="Netherlands", ch=["Doc","Article"],         views=172, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="A.P. Moller-Maersk",   ctry="Denmark",     ch=["Doc","Article"],         views=168, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Eaton",                 ctry="Ireland",     ch=["Doc","Video","Article"], views=167, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Novo Nordisk",          ctry="Denmark",     ch=["Doc","Article"],         views=159, clicks=4,    ctr=2.52, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="BMW Group",             ctry="Germany",     ch=["Doc","Article"],         views=139, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Zalando",               ctry="Germany",     ch=["Video","Article"],       views=132, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Scania Group",          ctry="Sweden",      ch=["Doc","Video"],           views=125, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="LSEG",                  ctry="UK",          ch=["Doc"],                   views=116, clicks=3,    ctr=2.59, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Volvo Group",           ctry="Sweden",      ch=["Video","Article"],       views=93,  clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="ASML",                  ctry="Netherlands", ch=["Video","Article"],       views=84,  clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Nordea",                ctry="Denmark",     ch=["Video","Article"],       views=78,  clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Delivery Hero",         ctry="Germany",     ch=["Article"],              views=59,  clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Zurich Insurance",      ctry="Switzerland", ch=["Video"],                views=45,  clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
]

UNIFY_SOUTH = [
    dict(co="Akbank",       ctry="Turkey", ch=["Doc","Video"],  views=201, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Qatar Airways", ctry="Qatar", ch=["Doc","Video"],  views=129, clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Emirates NBD",  ctry="UAE",   ch=["Doc"],          views=97,  clicks=3,    ctr=3.09, op=None, lead=None, ltitle=None, ldate=None),
    dict(co="Valeo",         ctry="France",ch=["Video"],        views=24,  clicks=None, ctr=None, op=None, lead=None, ltitle=None, ldate=None),
]

G2_NORTH = [
    # ── High ──
    dict(co="Yandex", ctry="Russian Federation", activity="High", visitor="United Kingdom", last="6 days ago", days=6, visitors=None, signals=5),
    dict(co="Yara", ctry="Norway", activity="High", visitor="Denmark", last="~4 weeks ago", days=28, visitors=None, signals=7),
    dict(co="T-Systems International", ctry="Germany", activity="High", visitor="Slovakia", last="~5 weeks ago", days=34, visitors=None, signals=10),
    # ── Medium ──
    dict(co="Proximus", ctry="Belgium", activity="Medium", visitor="Belgium", last="1 day ago", days=1, visitors=None, signals=5),
    dict(co="NHS Fife", ctry="United Kingdom", activity="Medium", visitor="United Kingdom", last="1 day ago", days=1, visitors=None, signals=4),
    dict(co="Nuuday", ctry="Denmark", activity="Medium", visitor="Denmark", last="4 days ago", days=4, visitors=None, signals=4),
    dict(co="Acronis", ctry="Switzerland", activity="Medium", visitor="Serbia", last="~3 weeks ago", days=21, visitors=None, signals=4),
    dict(co="DHL", ctry="Germany", activity="Medium", visitor="South Africa", last="~4 weeks ago", days=25, visitors=None, signals=5),
    dict(co="Novo Nordisk", ctry="Denmark", activity="Medium", visitor="France", last="~4 weeks ago", days=26, visitors=None, signals=4),
    dict(co="Vinted", ctry="Lithuania", activity="Medium", visitor="Sweden", last="~5 weeks ago", days=37, visitors=None, signals=5),
    dict(co="University of Zurich", ctry="Switzerland", activity="Medium", visitor="Switzerland", last="~2 months ago", days=46, visitors=None, signals=6),
    dict(co="PwC", ctry="United Kingdom", activity="Medium", visitor="France", last="~2 months ago", days=53, visitors=None, signals=4),
    dict(co="O2 (Telefónica UK)", ctry="United Kingdom", activity="Medium", visitor="Poland", last="~2 months ago", days=53, visitors=None, signals=5),
    dict(co="Sage", ctry="United Kingdom", activity="Medium", visitor="Germany", last="~2 months ago", days=54, visitors=None, signals=3),
    dict(co="Visma", ctry="Norway", activity="Medium", visitor="Sweden", last="~2 months ago", days=60, visitors=None, signals=3),
    dict(co="Datev eG", ctry="Germany", activity="Medium", visitor="Germany", last="~2 months ago", days=62, visitors=None, signals=7),
    dict(co="Bosch", ctry="Germany", activity="Medium", visitor="Germany", last="~2 months ago", days=75, visitors=None, signals=4),
    # ── Low ──
    dict(co="Politechnika Czstochowska", ctry="Poland", activity="Low", visitor="Poland", last="2 days ago", days=2, visitors=None, signals=3),
    dict(co="University of Turku", ctry="Finland", activity="Low", visitor="Finland", last="6 days ago", days=6, visitors=None, signals=3),
    dict(co="Siemens", ctry="Germany", activity="Low", visitor="Germany", last="6 days ago", days=6, visitors=None, signals=4),
    dict(co="Foundever", ctry="Luxembourg", activity="Low", visitor="Morocco", last="~12 days ago", days=12, visitors=None, signals=3),
    dict(co="Coleg Llandrillo; Grwp LlandrilloMenai", ctry="United Kingdom", activity="Low", visitor="United Kingdom", last="~2 months ago", days=44, visitors=None, signals=3),
    dict(co="Westcon-Comstor", ctry="United Kingdom", activity="Low", visitor="United Arab Emirates", last="~2 months ago", days=49, visitors=None, signals=3),
    dict(co="DEPT", ctry="Netherlands", activity="Low", visitor="United Kingdom", last="~2 months ago", days=52, visitors=None, signals=3),
    dict(co="UNILIN", ctry="Belgium", activity="Low", visitor="Belgium", last="~2 months ago", days=60, visitors=None, signals=3),
    dict(co="Mainova", ctry="Germany", activity="Low", visitor="Germany", last="~2 months ago", days=61, visitors=None, signals=3),
    dict(co="ORTEC", ctry="Netherlands", activity="Low", visitor="Greece", last="~2 months ago", days=74, visitors=None, signals=4),
    dict(co="Pepperl+Fuchs", ctry="Germany", activity="Low", visitor="Germany", last="~3 months ago", days=80, visitors=None, signals=6),
    dict(co="IFS", ctry="Sweden", activity="Low", visitor="Türkiye", last="~3 months ago", days=88, visitors=None, signals=3),
]

G2_SOUTH = [
    # ── High ──
    dict(co="Thales", ctry="France", activity="High", visitor="France", last="~10 days ago", days=10, visitors=None, signals=7),
    dict(co="Naval Group", ctry="France", activity="High", visitor="France", last="~5 weeks ago", days=33, visitors=None, signals=6),
    dict(co="Check Point", ctry="Israel", activity="High", visitor="Israel", last="~2 months ago", days=46, visitors=None, signals=6),
    # ── Medium ──
    dict(co="Schneider Electric", ctry="France", activity="Medium", visitor="France", last="~3 weeks ago", days=19, visitors=None, signals=4),
    dict(co="Cognyte", ctry="Israel", activity="Medium", visitor="Israel", last="~4 weeks ago", days=26, visitors=None, signals=5),
    dict(co="GMG", ctry="United Arab Emirates", activity="Medium", visitor="United Arab Emirates", last="~6 weeks ago", days=39, visitors=None, signals=4),
    dict(co="Tanta University", ctry="Egypt", activity="Medium", visitor="Egypt", last="~2 months ago", days=53, visitors=None, signals=5),
    dict(co="Dnata", ctry="United Arab Emirates", activity="Medium", visitor="Switzerland", last="~3 months ago", days=77, visitors=None, signals=5),
    dict(co="SFR", ctry="France", activity="Medium", visitor="France", last="~3 months ago", days=79, visitors=None, signals=5),
    # ── Low ──
    dict(co="Türk Telekom", ctry="Türkiye", activity="Low", visitor="Türkiye", last="3 days ago", days=3, visitors=None, signals=6),
    dict(co="Orange", ctry="France", activity="Low", visitor="France", last="~12 days ago", days=12, visitors=None, signals=11),
    dict(co="Sharaf DG", ctry="United Arab Emirates", activity="Low", visitor="United Arab Emirates", last="~13 days ago", days=13, visitors=None, signals=3),
    dict(co="Togg", ctry="Türkiye", activity="Low", visitor="Türkiye", last="~4 weeks ago", days=30, visitors=None, signals=4),
    dict(co="monday.com", ctry="Israel", activity="Low", visitor="Israel", last="~5 weeks ago", days=32, visitors=None, signals=3),
    dict(co="Ben Gurion University of Negev", ctry="Israel", activity="Low", visitor="Israel", last="~2 months ago", days=45, visitors=None, signals=3),
    dict(co="Zagrebacka banka", ctry="Croatia", activity="Low", visitor="Croatia", last="~2 months ago", days=53, visitors=None, signals=3),
    dict(co="CTT", ctry="Portugal", activity="Low", visitor="Portugal", last="~2 months ago", days=54, visitors=None, signals=3),
    dict(co="Rothschild & Co", ctry="France", activity="Low", visitor="France", last="~2 months ago", days=62, visitors=None, signals=3),
    dict(co="Trendyol", ctry="Türkiye", activity="Low", visitor="Türkiye", last="~2 months ago", days=65, visitors=None, signals=15),
    dict(co="e&", ctry="United Arab Emirates", activity="Low", visitor="United Arab Emirates", last="~2 months ago", days=73, visitors=None, signals=3),
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
    return f'<span style="font-size:12px;color:#4b5563;">{len(ch)}</span>'

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
          <td class="r" data-v="{sv(d['views'])}">{fmt_views(d['views'])}</td>
          <td class="r" data-v="{sv(d['clicks'])}">{fmt_clicks(d['clicks'])}</td>
          <td class="r" data-v="{sv(d['ctr'])}">{fmt_ctr(d['ctr'])}</td>
          <td class="r" data-v="{sv(d['op'])}">{fmt_open(d['op'], has_clicks, inmail_only)}</td>
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
    <th class="r" data-col="1">AD VIEWS <span class="si">↕</span></th>
    <th class="r" data-col="2">AD CLICKS <span class="si">↕</span></th>
    <th class="r" data-col="3">CTR <span class="si">↕</span></th>
    <th class="r" data-col="4">INMAIL OPEN RATE <span class="si">↕</span></th>
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
        date_label = "Apr 1 – Jul 12, 2026"
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

