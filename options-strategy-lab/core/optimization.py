from __future__ import annotations
import itertools
import pandas as pd
import numpy as np


def grid_search_demo() -> pd.DataFrame:
    rows = []
    for rsi, stop, wing in itertools.product([30, 35, 40], [0.8, 1.0, 1.2], [100, 150, 200]):
        sharpe = 0.6 + (40-rsi)*0.02 + (1.2-stop)*0.15 + (200-wing)*0.001 + np.random.default_rng(rsi+int(stop*10)+wing).normal(0, 0.05)
        dd = -6 - (wing/100)*1.2 - stop*2
        rows.append({"RSI Entry": rsi, "Stop Mult": stop, "Wing Width": wing, "Sharpe": round(sharpe,2), "Max DD %": round(dd,2)})
    return pd.DataFrame(rows).sort_values(["Sharpe", "Max DD %"], ascending=[False, False]).reset_index(drop=True)
