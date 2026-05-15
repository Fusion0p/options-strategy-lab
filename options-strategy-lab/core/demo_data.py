from __future__ import annotations
import numpy as np
import pandas as pd
from datetime import datetime


def get_market_snapshot():
    return [
        {"label": "Research Universe", "value": "NIFTY · BANKNIFTY · FINNIFTY", "foot": "Weekly & monthly expiries ready", "tone": "neu"},
        {"label": "Signal Breadth", "value": "11 Factors", "foot": "+ Technical, vol, sentiment fusion", "tone": "pos"},
        {"label": "Risk Lens", "value": "VaR 99% · ES", "foot": "Stress scenarios included", "tone": "neu"},
        {"label": "Execution Realism", "value": "Costs + Slippage", "foot": "Bid-ask spread aware", "tone": "pos"},
    ]


def get_strategy_marketplace():
    return [
        {"name":"Adaptive Iron Condor","regime":"Sideways / Low Vol","description":"Delta-filtered short premium system with volatility guardrails and dynamic wing widths.","cagr":"24.8%","sharpe":"1.68","max_dd":"-8.4%","win_rate":"71%"},
        {"name":"Event Straddle Breakout","regime":"High Vol","description":"Long gamma preset for event weeks using sentiment acceleration and VWAP confirmation.","cagr":"18.2%","sharpe":"1.24","max_dd":"-11.6%","win_rate":"48%"},
        {"name":"Trend Bull Put Spread","regime":"Bull Trend","description":"EMA and Supertrend aligned bullish credit spread model with tail-risk stop logic.","cagr":"21.1%","sharpe":"1.41","max_dd":"-9.2%","win_rate":"67%"},
        {"name":"Weekly Short Strangle","regime":"Rangebound","description":"Volatility premium capture with intraday hedge triggers and margin-aware sizing.","cagr":"27.6%","sharpe":"1.53","max_dd":"-13.7%","win_rate":"69%"},
        {"name":"Calendar Carry","regime":"Low RV / High IV","description":"Near-far expiry relative value play targeting term-structure mean reversion.","cagr":"16.4%","sharpe":"1.17","max_dd":"-7.9%","win_rate":"58%"},
        {"name":"Covered Call Yield","regime":"Moderate Bull","description":"Portfolio overlay strategy for stock holdings with drawdown-aware overwrite timing.","cagr":"14.5%","sharpe":"1.09","max_dd":"-10.3%","win_rate":"62%"},
    ]


def make_price_series(seed: int = 42, periods: int = 180, start: str = "2024-01-01") -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start=start, periods=periods)
    drift = 0.0007
    vol = 0.012
    rets = rng.normal(drift, vol, len(dates))
    close = 22000 * np.exp(np.cumsum(rets))
    high = close * (1 + rng.uniform(0.002, 0.012, len(close)))
    low = close * (1 - rng.uniform(0.002, 0.012, len(close)))
    open_ = close * (1 + rng.normal(0, 0.004, len(close)))
    volume = rng.integers(120000, 380000, len(close))
    return pd.DataFrame({"date": dates, "open": open_, "high": high, "low": low, "close": close, "volume": volume})


def make_trade_log(seed: int = 9, trades: int = 36) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range("2024-01-04", periods=trades, freq="7B")
    strategies = ["Iron Condor", "Short Strangle", "Bull Put Spread", "Long Straddle"]
    gross = rng.normal(9500, 18000, trades)
    costs = rng.uniform(300, 1200, trades)
    net = gross - costs
    pnl_pct = net / rng.uniform(180000, 320000, trades)
    win = net > 0
    regime = rng.choice(["Bull", "Bear", "Sideways", "High Vol"], size=trades, p=[0.28,0.18,0.34,0.20])
    return pd.DataFrame({
        "entry_date": dates,
        "exit_date": dates + pd.to_timedelta(rng.integers(1, 5, trades), unit="D"),
        "strategy": rng.choice(strategies, trades),
        "regime": regime,
        "gross_pnl": gross.round(2),
        "costs": costs.round(2),
        "net_pnl": net.round(2),
        "return_pct": (pnl_pct*100).round(2),
        "winner": win,
    })
