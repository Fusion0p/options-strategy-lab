import streamlit as st
import pandas as pd
import plotly.express as px
from core.theme import inject_global_styles
from core.greeks import black_scholes_greeks
from core.utils import var_es

inject_global_styles()
st.title("Greeks & Risk Engine")
st.caption("Estimate option Greeks, portfolio exposure, downside risk, and scenario losses from a single risk console.")

c1, c2, c3, c4, c5 = st.columns(5)
spot = c1.number_input("Spot", 1000.0, 100000.0, 22450.0, 50.0)
strike = c2.number_input("Strike", 1000.0, 100000.0, 22500.0, 50.0)
dte = c3.slider("Days to Expiry", 1, 90, 14)
rate = c4.slider("Risk-free Rate", 0.01, 0.12, 0.07, 0.005)
vol = c5.slider("Implied Vol", 0.05, 0.80, 0.18, 0.01)
option_type = st.radio("Option Type", ["call", "put"], horizontal=True)
res = black_scholes_greeks(spot, strike, dte/365, rate, vol, option_type)

m1, m2, m3, m4, m5, m6 = st.columns(6)
for col, (label, value) in zip((m1, m2, m3, m4, m5, m6), [("Price", res.price), ("Delta", res.delta), ("Gamma", res.gamma), ("Theta", res.theta), ("Vega", res.vega), ("Rho", res.rho)]):
    col.metric(label, f"{value:.4f}")

scenario_spots = [spot * (1 + x/100) for x in [-10, -5, -2, 0, 2, 5, 10]]
scenario_vols = [max(vol + x, 0.05) for x in [-0.06, -0.03, 0, 0.03, 0.06]]
rows = []
for s in scenario_spots:
    for v in scenario_vols:
        price = black_scholes_greeks(s, strike, dte/365, rate, v, option_type).price
        rows.append({"Spot Shock": round((s/spot-1)*100, 1), "IV Shock": round((v-vol)*100, 1), "Option Px": round(price, 2)})
heat = pd.DataFrame(rows).pivot(index='IV Shock', columns='Spot Shock', values='Option Px')
fig = px.imshow(heat, text_auto='.1f', color_continuous_scale='RdYlGn', aspect='auto', title='Scenario Heatmap: Option Price')
fig.update_layout(template='plotly_dark', height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

returns = pd.Series([-0.018, 0.007, -0.024, 0.013, -0.009, 0.004, -0.031, 0.016, 0.009, -0.012, 0.005])
var95, es95 = var_es(returns, 0.95)
left, right = st.columns(2)
with left:
    st.markdown("### Portfolio Controls")
    st.markdown("""
- Net Greeks exposure monitoring for delta, gamma, theta, vega, and rho.
- Margin approximation for short premium trades and spread offsets.
- Daily stop-loss, max loss cap, and regime-aware size reduction.
- Historical stress templates for 2020 crash and 2022 volatility spike.
""")
with right:
    st.markdown("### Tail Risk Snapshot")
    st.metric("VaR 95%", f"{var95*100:.2f}%")
    st.metric("Expected Shortfall 95%", f"{es95*100:.2f}%")
    st.warning("Stress test example: a -10% index shock with +6 vol points materially raises convexity risk for short gamma structures.")
