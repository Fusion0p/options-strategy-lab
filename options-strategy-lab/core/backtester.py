from __future__ import annotations
import pandas as pd
from core.demo_data import make_trade_log
from core.analytics import compute_performance_metrics


def run_demo_backtest(strategy_name: str, capital: float) -> tuple[pd.DataFrame, dict]:
    trade_log = make_trade_log(seed=abs(hash(strategy_name)) % (2**32))
    metrics = compute_performance_metrics(trade_log, initial_capital=capital)
    return trade_log, metrics
