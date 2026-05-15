# Options Strategy Lab

Options Strategy Lab is a production-style Streamlit application for options strategy research on Indian markets. It combines strategy backtesting, multi-factor signal overlays, Greeks risk analytics, manual trade replay, optimization, and export workflows in a dark, recruiter-friendly interface.

## Project structure

```text
options-strategy-lab/
├── app.py
├── pages/
├── core/
├── data/
├── assets/
├── .streamlit/
├── requirements.txt
├── .gitignore
└── README.md
```

## Features

- Landing page with a strong product message, live-style visual panel, quick presets, and strategy marketplace
- Strategy Builder for iron condors, strangles, straddles, bull put spreads, covered calls, and calendar spreads
- Manual Trade Simulator with candle replay workflow, strike selection mode, option pricing snapshot, and cumulative trade journal
- Greeks & Risk Engine using Black-Scholes pricing with scenario heatmaps, VaR, and Expected Shortfall
- Analytics page with parameter search, Monte Carlo distribution view, and walk-forward guidance
- Export hub for trade logs and summary reports

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push the folder to a GitHub repository.
2. In Streamlit Community Cloud, create a new app pointing to `app.py`.
3. Ensure `requirements.txt` is present in the root of the repo.
4. Set any data or API secrets in Streamlit secrets management if you replace the demo layer with live feeds.

## Production upgrade path

- Replace synthetic demo data with NSEPy, broker APIs, or compliant market data feeds
- Add persistence for user workspaces, saved backtests, and manual trade journals
- Introduce authentication, role-based workspaces, and scheduled data refresh jobs
- Generate richer PDF and Excel reports using background tasks
- Expand sentiment modelling with transformer-based scoring and event tagging

## Notes

The current build is fully functional as a polished demo and architecture template. It is intentionally modular so that pricing models, data connectors, optimization engines, and reporting components can be upgraded without changing the app shell.
