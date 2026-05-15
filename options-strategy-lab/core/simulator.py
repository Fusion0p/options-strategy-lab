from __future__ import annotations
import pandas as pd
from core.greeks import black_scholes_greeks


def option_snapshot(spot: float, moneyness: str, days_to_expiry: int, iv: float, option_type: str):
    shift = {"ITM": -200, "ATM": 0, "OTM": 200}.get(moneyness, 0)
    strike = round((spot + shift) / 50) * 50
    greeks = black_scholes_greeks(spot=spot, strike=strike, time_to_expiry=max(days_to_expiry,1)/365, rate=0.07, vol=iv, option_type=option_type.lower())
    bid = round(max(greeks.price * 0.992, 0.5), 2)
    ask = round(greeks.price * 1.008, 2)
    return strike, greeks, bid, ask


def build_manual_trade(entry_row: pd.Series, exit_row: pd.Series, quantity: int, option_type: str, moneyness: str, iv: float, slippage: float, cost_per_lot: float):
    strike, g, bid, ask = option_snapshot(entry_row['close'], moneyness, 14, iv, option_type)
    _, g2, bid2, ask2 = option_snapshot(exit_row['close'], moneyness, 7, iv * 1.02, option_type)
    entry_price = ask * (1 + slippage)
    exit_price = bid2 * (1 - slippage)
    gross = (exit_price - entry_price) * quantity
    costs = cost_per_lot
    net = gross - costs
    return {
        'Entry Date': pd.to_datetime(entry_row['date']).date().isoformat(),
        'Exit Date': pd.to_datetime(exit_row['date']).date().isoformat(),
        'Strike': strike,
        'Type': option_type,
        'Moneyness': moneyness,
        'Qty': quantity,
        'Entry Px': round(entry_price, 2),
        'Exit Px': round(exit_price, 2),
        'Gross P&L': round(gross, 2),
        'Net P&L': round(net, 2),
        'Return %': round((net / max(entry_price * quantity, 1)) * 100, 2),
        'Holding Days': int((pd.to_datetime(exit_row['date']) - pd.to_datetime(entry_row['date'])).days),
        'Delta': round(g.delta, 4),
        'Gamma': round(g.gamma, 5),
        'Theta': round(g.theta, 4),
        'Vega': round(g.vega, 4),
        'Bid/Ask': f"{bid:.2f} / {ask:.2f}",
    }
