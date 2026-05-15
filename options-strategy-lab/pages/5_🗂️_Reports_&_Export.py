import streamlit as st
from core.theme import inject_global_styles
from core.demo_data import make_trade_log
from core.analytics import compute_performance_metrics
from core.report_builder import to_csv_bytes, summary_text

inject_global_styles()
st.title("Reports & Export")
st.caption("Download trade logs, summary metrics, and recruiter-friendly documentation from one export hub.")

trade_log = make_trade_log(seed=25, trades=40)
metrics = compute_performance_metrics(trade_log)

st.subheader("Backtest Summary")
st.text(summary_text(metrics))
st.dataframe(trade_log, use_container_width=True, hide_index=True)

st.download_button("Download trade log CSV", data=to_csv_bytes(trade_log), file_name='options_strategy_lab_trade_log.csv', mime='text/csv', use_container_width=True)
st.download_button("Download summary TXT", data=summary_text(metrics).encode('utf-8'), file_name='options_strategy_lab_summary.txt', mime='text/plain', use_container_width=True)

st.markdown("### Production Deployment Checklist")
st.markdown("""
1. Replace synthetic loaders with NSEPy or broker/NSE-compliant data connectors.
2. Persist backtests, trade journals, and reports to a database or object store.
3. Schedule daily data refresh and signal computation jobs.
4. Add PDF/XLSX generation services and authenticated user workspaces.
""")
