import streamlit as st


def logo_svg() -> str:
    return """
    <svg width='18' height='18' viewBox='0 0 64 64' fill='none' xmlns='http://www.w3.org/2000/svg' aria-label='Options Strategy Lab logo'>
      <rect x='6' y='8' width='52' height='48' rx='12' stroke='currentColor' stroke-width='4'/>
      <path d='M18 40L28 28L36 34L46 20' stroke='currentColor' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'/>
      <circle cx='46' cy='20' r='4' fill='currentColor'/>
    </svg>
    """


def hero_metrics_html() -> str:
    items = [
        ("12+", "strategy templates"),
        ("5", "portfolio Greeks"),
        ("99th", "stress percentile"),
        ("1-click", "PDF/XLSX export"),
    ]
    return "".join([f"<div class='hero-chip'><strong>{a}</strong><span>{b}</span></div>" for a, b in items])


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --bg:#0b1020; --surface:#10182b; --surface2:#141f37; --border:rgba(173,194,255,.14);
            --text:#e8edf7; --muted:#93a4c3; --accent:#35c2ff; --accent2:#7c5cff; --success:#1fd18b; --warn:#f59e0b;
            --danger:#ef4444; --shadow:0 20px 60px rgba(3, 10, 28, .45); --radius:20px;
        }
        .stApp { background: radial-gradient(circle at top right, rgba(53,194,255,.10), transparent 20%), linear-gradient(180deg, #0b1020 0%, #0d1425 100%); color: var(--text); }
        .main .block-container { padding-top: 1.25rem; padding-bottom: 2rem; max-width: 1360px; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #0b1020, #0e1730); border-right: 1px solid var(--border); }
        h1,h2,h3,h4,p,label,div,span { color: var(--text); }
        .osl-shell { margin-bottom: 1.2rem; }
        .osl-hero { display:grid; grid-template-columns: 1.15fr .85fr; gap: 1.25rem; padding: 1.4rem 0 1rem; align-items: stretch; }
        .osl-hero-copy, .osl-terminal, .kpi-card, .market-card { background: linear-gradient(180deg, rgba(16,24,43,.92), rgba(12,19,33,.92)); border:1px solid var(--border); border-radius: 24px; box-shadow: var(--shadow); }
        .osl-hero-copy { padding: 1.5rem; }
        .osl-badge { display:inline-flex; align-items:center; gap:.6rem; padding:.45rem .8rem; border:1px solid rgba(53,194,255,.24); background: rgba(53,194,255,.08); border-radius:999px; font-size:.86rem; color:#d9f5ff; }
        .osl-badge svg { color: var(--accent); }
        .osl-hero-copy h1 { font-size: clamp(2.2rem, 2rem + 1.5vw, 3.7rem); line-height:1.02; margin:.9rem 0 .75rem; letter-spacing:-.03em; }
        .osl-subtitle { max-width: 66ch; color: var(--muted); font-size: 1rem; }
        .osl-hero-actions { display:flex; gap:.8rem; margin: 1.15rem 0; }
        .osl-btn { text-decoration:none; padding:.85rem 1.05rem; border-radius:14px; font-weight:700; border:1px solid var(--border); display:inline-flex; align-items:center; justify-content:center; }
        .osl-btn-primary { background: linear-gradient(135deg, var(--accent), #1d9bf0); color:#06111f !important; }
        .osl-btn-secondary { background: rgba(124,92,255,.10); color:#d7d0ff !important; }
        .osl-hero-metrics { display:grid; grid-template-columns: repeat(4,1fr); gap:.7rem; }
        .hero-chip { padding:.8rem; border-radius:16px; background: rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.06); }
        .hero-chip strong { display:block; font-size:1rem; }
        .hero-chip span { color:var(--muted); font-size:.78rem; }
        .osl-hero-visual { position:relative; min-height: 100%; }
        .osl-glow { position:absolute; inset: 12% 16% auto auto; width:180px; height:180px; background: radial-gradient(circle, rgba(124,92,255,.35), transparent 65%); filter: blur(10px); }
        .osl-terminal { padding:1rem; height:100%; position:relative; overflow:hidden; }
        .osl-terminal-top { display:flex; align-items:center; gap:.45rem; color:var(--muted); font-size:.78rem; margin-bottom:1rem; }
        .osl-terminal-top span { width:10px; height:10px; border-radius:999px; background:#24314e; }
        .osl-terminal-top span:nth-child(1){ background:#ef4444; } .osl-terminal-top span:nth-child(2){ background:#f59e0b; } .osl-terminal-top span:nth-child(3){ background:#1fd18b; }
        .osl-code-block { border:1px solid rgba(255,255,255,.07); background: rgba(255,255,255,.02); border-radius:18px; padding:1rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; line-height:1.8; font-size:.93rem; }
        .k { color:#93a4c3; } .v { color:#d9f5ff; } .warn { color:#fcbf49; }
        .osl-mini-grid { display:grid; grid-template-columns:1fr 1fr; gap:.85rem; margin-top:.9rem; }
        .mini-card { padding:.9rem; border-radius:18px; background: rgba(255,255,255,.03); border:1px solid rgba(255,255,255,.06); }
        .mini-card label { font-size:.78rem; color:var(--muted); margin-bottom:.55rem; display:block; }
        .spark { height:84px; border-radius:14px; background: linear-gradient(180deg, rgba(53,194,255,.18), rgba(53,194,255,.02)); position:relative; overflow:hidden; }
        .spark:after { content:''; position:absolute; left:8px; right:8px; top:22px; height:36px; border-bottom:2px solid var(--accent); border-radius:60% 40% 35% 70% / 50% 30% 70% 50%; transform: skewX(-12deg); }
        .heatmap { height:84px; border-radius:14px; background: linear-gradient(90deg, rgba(124,92,255,.18), rgba(53,194,255,.18)); box-shadow: inset 0 0 0 1px rgba(255,255,255,.06); position:relative; }
        .heatmap:after { content:''; position:absolute; inset:8px; background: linear-gradient(90deg, rgba(255,255,255,.02) 50%, transparent 50%), linear-gradient(0deg, rgba(255,255,255,.02) 50%, transparent 50%); background-size: 22px 22px; }
        .kpi-card { padding: 1rem; }
        .kpi-label { font-size:.8rem; color:var(--muted); text-transform:uppercase; letter-spacing:.08em; }
        .kpi-value { font-size:1.65rem; font-weight:800; margin:.35rem 0; }
        .kpi-foot { font-size:.88rem; } .pos { color: var(--success); } .neg { color: #fca5a5; } .neu { color: var(--muted); }
        .market-card { padding:1rem; min-height: 220px; }
        .market-top { display:flex; justify-content:space-between; gap:.8rem; align-items:center; margin-bottom:.6rem; }
        .market-name { font-weight:800; }
        .market-badge { font-size:.76rem; color:#d9f5ff; padding:.25rem .55rem; border-radius:999px; background:rgba(53,194,255,.10); border:1px solid rgba(53,194,255,.18); }
        .market-card p { color:var(--muted); min-height: 54px; }
        .market-grid { display:grid; grid-template-columns:1fr 1fr; gap:.8rem; margin-top:.85rem; }
        .market-grid label { display:block; font-size:.76rem; color:var(--muted); margin-bottom:.15rem; }
        .stButton>button, .stDownloadButton>button { background: linear-gradient(135deg, var(--accent), #1d9bf0); color:#05111f; border:none; border-radius:14px; font-weight:800; }
        .stTextInput>div>div>input, .stNumberInput input, .stDateInput input, .stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div, .stTextArea textarea {
            background: rgba(255,255,255,.03) !important; color: var(--text) !important; border:1px solid var(--border) !important; border-radius: 12px !important;
        }
        [data-testid='stMetricValue'], [data-testid='stMetricLabel'] { color: var(--text); }
        div[data-testid="stDataFrame"] { border:1px solid var(--border); border-radius:18px; overflow:hidden; }
        @media (max-width: 980px) {
            .osl-hero { grid-template-columns: 1fr; }
            .osl-hero-metrics { grid-template-columns: repeat(2,1fr); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
