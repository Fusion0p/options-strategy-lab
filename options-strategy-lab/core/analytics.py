from __future__ import annotations
import numpy as np
import pandas as pd


def compute_performance_metrics(trade_log: pd.DataFrame, initial_capital: float = 500000) -> dict:
    if trade_log.empty:
        return {}
    equity = initial_capital + trade_log['net_pnl'].cumsum()
    returns = equity.pct_change().fillna(0)
    downside = returns[returns < 0]
    drawdown = equity / equity.cummax() - 1
    wins = trade_log.loc[trade_log['net_pnl'] > 0, 'net_pnl']
    losses = trade_log.loc[trade_log['net_pnl'] <= 0, 'net_pnl']
    return {
        'Total Return %': round((equity.iloc[-1] / initial_capital - 1) * 100, 2),
        'Sharpe': round((returns.mean() / (returns.std() + 1e-9)) * np.sqrt(252), 2),
        'Sortino': round((returns.mean() / (downside.std() + 1e-9)) * np.sqrt(252), 2),
        'Calmar': round(((equity.iloc[-1] / initial_capital - 1) / abs(drawdown.min() + 1e-9)), 2),
        'Max Drawdown %': round(drawdown.min() * 100, 2),
        'Win Rate %': round((trade_log['net_pnl'] > 0).mean() * 100, 2),
        'Profit Factor': round(wins.sum() / abs(losses.sum() + 1e-9), 2),
        'Expectancy': round(trade_log['net_pnl'].mean(), 2),
        'Average Win': round(wins.mean() if len(wins) else 0, 2),
        'Average Loss': round(losses.mean() if len(losses) else 0, 2),
        'Payoff Ratio': round((wins.mean() if len(wins) else 0) / abs((losses.mean() if len(losses) else -1)), 2),
    }


def monthly_returns_table(trade_log: pd.DataFrame) -> pd.DataFrame:
    df = trade_log.copy()
    df['month'] = pd.to_datetime(df['exit_date']).dt.to_period('M').astype(str)
    monthly = df.groupby('month')['return_pct'].sum().reset_index()
    monthly[['year', 'month_num']] = monthly['month'].str.split('-', expand=True)
    pivot = monthly.pivot(index='year', columns='month_num', values='return_pct').fillna(0)
    return pivot.round(2)
