import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from core.theme import inject_global_styles
from core.data_loader import load_market_data
from core.simulator import build_manual_trade

inject_global_styles()
st.title("Manual Trade Simulator")
st.caption("Replay historical candles, select entry and exit points, and inspect option pricing with Greeks at the moment of trade initiation.")

if 'manual_trades' not in st.session_state:
    st.session_state.manual_trades = []

c1, c2, c3 = st.columns(3)
symbol = c1.selectbox("Underlying", ["NIFTY", "BANKNIFTY", "FINNIFTY", "RELIANCE", "TCS"])
timeframe = c2.selectbox("Timeframe", ["Daily", "Hourly (synthetic)"])
window = c3.slider("History Window", 60, 220, 140, 10)

df = load_market_data(symbol).tail(window).reset_index(drop=True)
fig = go.Figure(data=[go.Candlestick(x=df['date'], open=df['open'], high=df['high'], low=df['low'], close=df['close'], increasing_line_color='#1fd18b', decreasing_line_color='#ef4444')])
fig.update_layout(template='plotly_dark', height=480, title=f'{symbol} Replay Chart', xaxis_rangeslider_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
    st.markdown("### Trade Ticket")
    t1, t2, t3, t4 = st.columns(4)
    entry_idx = t1.slider("Entry Candle", 0, len(df)-2, len(df)//3)
    exit_idx = t2.slider("Exit Candle", entry_idx+1, len(df)-1, min(entry_idx+5, len(df)-1))
    qty = t3.number_input("Quantity", 25, 5000, 50, 25)
    capital = t4.number_input("Capital", 25000, 5000000, 100000, 25000)
    x1, x2, x3, x4 = st.columns(4)
    option_type = x1.selectbox("Option Type", ["Call", "Put"])
    moneyness = x2.selectbox("Strike Mode", ["ATM", "ITM", "OTM"])
    iv = x3.slider("Implied Volatility", 0.08, 0.55, 0.18, 0.01)
    slippage = x4.slider("Slippage", 0.000, 0.020, 0.004, 0.001)
    cost = st.number_input("Transaction Cost / Lot", 0.0, 5000.0, 450.0, 50.0)
    if st.button("Add Manual Trade", use_container_width=True):
        trade = build_manual_trade(df.iloc[entry_idx], df.iloc[exit_idx], qty, option_type, moneyness, iv, slippage, cost)
        trade['Allocated Capital'] = capital
        st.session_state.manual_trades.append(trade)
        st.success("Trade added to replay journal.")

entry_row = df.iloc[entry_idx]
exit_row = df.iloc[exit_idx]
st.markdown(f"Selected window: **{pd.to_datetime(entry_row['date']).date()}** to **{pd.to_datetime(exit_row['date']).date()}**")

trade_df = pd.DataFrame(st.session_state.manual_trades)
if not trade_df.empty:
    top1, top2, top3, top4 = st.columns(4)
    top1.metric("Manual Trades", len(trade_df))
    top2.metric("Cumulative Net P&L", f"₹{trade_df['Net P&L'].sum():,.0f}")
    top3.metric("Average Return", f"{trade_df['Return %'].mean():.2f}%")
    top4.metric("Best Trade", f"₹{trade_df['Net P&L'].max():,.0f}")
    st.dataframe(trade_df, use_container_width=True, hide_index=True)
    pnl = trade_df['Net P&L'].cumsum()
    pnl_fig = go.Figure(go.Scatter(x=list(range(1, len(pnl)+1)), y=pnl, mode='lines+markers', line=dict(color='#35c2ff', width=3)))
    pnl_fig.update_layout(template='plotly_dark', title='Cumulative Replay P&L', height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title='Trade #', yaxis_title='₹')
    st.plotly_chart(pnl_fig, use_container_width=True)
else:
    st.info("Add one or more manual trades to build a replay journal and compare scenarios.")
