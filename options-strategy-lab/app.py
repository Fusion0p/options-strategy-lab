import streamlit as st
from datetime import date
from core.theme import inject_global_styles, hero_metrics_html, logo_svg
from core.demo_data import get_market_snapshot, get_strategy_marketplace

st.set_page_config(
    page_title="Options Strategy Lab",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

st.markdown(f"""
<div class='osl-shell'>
  <section class='osl-hero'>
    <div class='osl-hero-copy'>
      <div class='osl-badge'>{logo_svg()}<span>Recruiter-grade options research workstation</span></div>
      <h1>Options Strategy Lab</h1>
      <p class='osl-subtitle'>Backtest NSE options strategies, combine multi-factor signals, inspect Greeks, replay trades candle-by-candle, and stress-test portfolios in one professional research interface.</p>
      <div class='osl-hero-actions'>
        <a href='#quick-backtest' class='osl-btn osl-btn-primary'>Quick Backtest</a>
        <a href='#marketplace' class='osl-btn osl-btn-secondary'>Try Demo</a>
      </div>
      <div class='osl-hero-metrics'>{hero_metrics_html()}</div>
    </div>
    <div class='osl-hero-visual'>
      <div class='osl-glow'></div>
      <div class='osl-terminal'>
        <div class='osl-terminal-top'>
          <span></span><span></span><span></span>
          <strong>LIVE RESEARCH SNAPSHOT</strong>
        </div>
        <div class='osl-code-block'>
          <div><span class='k'>Strategy</span>: <span class='v'>Iron Condor</span></div>
          <div><span class='k'>Signal Stack</span>: RSI + Vol Regime + Sentiment</div>
          <div><span class='k'>Net Delta</span>: <span class='v'>-0.06</span> &nbsp; <span class='k'>Theta</span>: <span class='v'>+184</span></div>
          <div><span class='k'>Max DD</span>: <span class='v warn'>-8.4%</span> &nbsp; <span class='k'>Sharpe</span>: <span class='v'>1.68</span></div>
        </div>
        <div class='osl-mini-grid'>
          <div class='mini-card'><label>Equity Curve</label><div class='spark spark-up'></div></div>
          <div class='mini-card'><label>Greeks Heatmap</label><div class='heatmap'></div></div>
        </div>
      </div>
    </div>
  </section>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
snapshot = get_market_snapshot()
for col, item in zip((col1, col2, col3, col4), snapshot):
    col.markdown(
        f"""
        <div class='kpi-card'>
          <div class='kpi-label'>{item['label']}</div>
          <div class='kpi-value'>{item['value']}</div>
          <div class='kpi-foot {item['tone']}'>{item['foot']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div id='quick-backtest'></div>", unsafe_allow_html=True)
st.markdown("## Quick Backtest")
left, right = st.columns([1.35, 1])
with left:
    st.markdown("Use the pages in the sidebar to run a full backtest, inspect portfolio Greeks, optimize parameters, and replay historical trades. This landing page is built to explain the product instantly and drive users into analysis within seconds.")
    with st.container(border=True):
        c1, c2, c3, c4 = st.columns(4)
        underlying = c1.selectbox("Underlying", ["NIFTY", "BANKNIFTY", "FINNIFTY", "RELIANCE", "HDFCBANK"])
        strategy = c2.selectbox("Preset", ["Iron Condor", "Short Strangle", "Bull Put Spread", "Long Straddle"])
        regime = c3.selectbox("Regime", ["Adaptive", "Low Vol", "High Vol", "Bull Trend", "Sideways"])
        capital = c4.number_input("Capital (₹)", min_value=100000, max_value=10000000, value=500000, step=50000)
        if st.button("Launch research workflow", use_container_width=True):
            st.success(f"Preset loaded: {strategy} on {underlying} with {regime} filters and ₹{capital:,.0f} capital.")
with right:
    st.markdown("### Feature Stack")
    st.markdown("""
- Multi-strategy backtesting for spreads, straddles, strangles, covered calls, and calendar structures.
- Portfolio Greeks engine with VaR, Expected Shortfall, margin view, and scenario shocks.
- Manual Trade Simulator for candle-click entry/exit analysis with option pricing snapshots.
- Walk-forward validation, Monte Carlo risk envelopes, and strategy optimization.
""")

st.markdown("<div id='marketplace'></div>", unsafe_allow_html=True)
st.markdown("## Strategy Marketplace")
market = get_strategy_marketplace()
cols = st.columns(3)
for idx, strat in enumerate(market):
    with cols[idx % 3]:
        st.markdown(
            f"""
            <div class='market-card'>
              <div class='market-top'>
                <span class='market-name'>{strat['name']}</span>
                <span class='market-badge'>{strat['regime']}</span>
              </div>
              <p>{strat['description']}</p>
              <div class='market-grid'>
                <div><label>CAGR</label><strong>{strat['cagr']}</strong></div>
                <div><label>Sharpe</label><strong>{strat['sharpe']}</strong></div>
                <div><label>Max DD</label><strong>{strat['max_dd']}</strong></div>
                <div><label>Win Rate</label><strong>{strat['win_rate']}</strong></div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("## Folder Structure")
st.code('''
options-strategy-lab/
├── app.py
├── pages/
│   ├── 1_📘_Strategy_Builder.py
│   ├── 2_🎯_Manual_Trade_Simulator.py
│   ├── 3_🧮_Greeks_&_Risk_Engine.py
│   ├── 4_📊_Analytics_&_Optimization.py
│   └── 5_🗂️_Reports_&_Export.py
├── core/
│   ├── __init__.py
│   ├── analytics.py
│   ├── backtester.py
│   ├── data_loader.py
│   ├── demo_data.py
│   ├── greeks.py
│   ├── optimization.py
│   ├── report_builder.py
│   ├── sentiment.py
│   ├── simulator.py
│   ├── strategies.py
│   ├── theme.py
│   └── utils.py
├── data/
│   └── sample_news.csv
├── assets/
│   └── architecture.mmd
├── .streamlit/
│   └── config.toml
├── requirements.txt
├── README.md
└── .gitignore
''')

st.info(f"Demo environment initialised for {date.today().isoformat()}. Open the sidebar pages to explore the full workflow.")
