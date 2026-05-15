import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from core.theme import inject_global_styles
from core.backtester import run_demo_backtest
from core.analytics import monthly_returns_table
from core.strategies import STRATEGY_LIBRARY

inject_global_styles()
st.title("Strategy Builder & Backtester")
st.caption("Build strategy presets, fuse signals, and evaluate realistic trade performance for Indian options markets.")

with st.container(border=True):
    c1, c2, c3, c4 = st.columns(4)
    strategy = c1.selectbox("Strategy", list(STRATEGY_LIBRARY))
    symbol = c2.selectbox("Underlying", ["NIFTY", "BANKNIFTY", "FINNIFTY", "RELIANCE", "SBIN"])
    expiry = c3.selectbox("Expiry Type", ["Weekly", "Monthly"])
    capital = c4.number_input("Capital", 100000, 10000000, 500000, 50000)
    d1, d2, d3, d4 = st.columns(4)
    d1.multiselect("Technical Signals", ["RSI", "Bollinger Bands", "EMA", "VWAP", "Supertrend"], default=["RSI", "EMA"])
    d2.selectbox("Volatility Regime", ["Adaptive", "Low IV", "High IV", "Term Structure"])
    d3.selectbox("Sentiment Filter", ["Off", "Headline NLP", "News + Social Composite"])
    d4.slider("Position Risk %", 0.5, 5.0, 1.5, 0.5)
    run = st.button("Run Backtest", use_container_width=True)

trade_log, metrics = run_demo_backtest(strategy, capital)
if run:
    st.success(f"Backtest finished for {strategy} on {symbol} {expiry.lower()} expiries.")

mc1, mc2, mc3, mc4, mc5 = st.columns(5)
for col, (k, v) in zip((mc1, mc2, mc3, mc4, mc5), list(metrics.items())[:5]):
    col.metric(k, v)

trade_log = trade_log.copy()
trade_log['equity'] = capital + trade_log['net_pnl'].cumsum()
trade_log['drawdown_pct'] = (trade_log['equity'] / trade_log['equity'].cummax() - 1) * 100

left, right = st.columns([1.35, 1])
with left:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=trade_log['exit_date'], y=trade_log['equity'], mode='lines', name='Strategy', line=dict(color='#35c2ff', width=3)))
    fig.add_trace(go.Scatter(x=trade_log['exit_date'], y=[capital*(1+i*0.004) for i in range(len(trade_log))], mode='lines', name='NIFTY Buy & Hold', line=dict(color='#7c5cff', width=2, dash='dot')))
    fig.update_layout(template='plotly_dark', title='Equity Curve vs Benchmark', height=420, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)
with right:
    dd_fig = px.area(trade_log, x='exit_date', y='drawdown_pct', title='Underwater Curve', color_discrete_sequence=['#ef4444'])
    dd_fig.update_layout(template='plotly_dark', height=420, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(dd_fig, use_container_width=True)

st.subheader("Trade Log")
st.dataframe(trade_log, use_container_width=True, hide_index=True)

st.subheader("Monthly Return Heatmap")
heat = monthly_returns_table(trade_log)
if not heat.empty:
    hm = px.imshow(heat, text_auto='.2f', aspect='auto', color_continuous_scale='Tealgrn')
    hm.update_layout(template='plotly_dark', height=340, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(hm, use_container_width=True)

with st.expander("Built-in strategy notes"):
    for name, desc in STRATEGY_LIBRARY.items():
        st.markdown(f"- **{name}** — {desc}")
