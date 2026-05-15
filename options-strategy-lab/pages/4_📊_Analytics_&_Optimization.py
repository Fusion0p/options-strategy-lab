import streamlit as st
import pandas as pd
import plotly.express as px
from core.theme import inject_global_styles
from core.demo_data import make_trade_log
from core.optimization import grid_search_demo
from core.analytics import compute_performance_metrics
import numpy as np

inject_global_styles()
st.title("Analytics, Walk-Forward & Optimization")
st.caption("Study robustness with parameter search, out-of-sample style validation, and Monte Carlo-inspired forward risk views.")

trade_log = make_trade_log(seed=17, trades=48)
metrics = compute_performance_metrics(trade_log)
row = st.columns(4)
for col, (k, v) in zip(row, list(metrics.items())[:4]):
    col.metric(k, v)

left, right = st.columns([1.05, 1])
with left:
    opt = grid_search_demo()
    st.subheader("Grid Search Leaderboard")
    st.dataframe(opt.head(10), use_container_width=True, hide_index=True)
    scatter = px.scatter(opt, x='Max DD %', y='Sharpe', color='Wing Width', size='Stop Mult', hover_data=['RSI Entry'], title='Parameter Frontier')
    scatter.update_layout(template='plotly_dark', height=360, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(scatter, use_container_width=True)
with right:
    mc = pd.DataFrame({
        'Path': [f'P{i+1}' for i in range(50)],
        'Final Return %': [round(v, 2) for v in np.random.default_rng(5).normal(13, 9, 50)]
    })
    hist = px.histogram(mc, x='Final Return %', nbins=18, color_discrete_sequence=['#35c2ff'], title='Monte Carlo Forward Return Distribution')
    hist.update_layout(template='plotly_dark', height=360, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(hist, use_container_width=True)
    st.markdown("### Walk-Forward Notes")
    st.markdown("""
- Train on rolling windows, validate on the next expiry cycle.
- Track parameter drift and reject unstable combinations.
- Compare in-sample vs out-of-sample Sharpe, drawdown, and turnover.
- Favor robust plateaus over isolated sharp peaks in the parameter map.
""")
