from __future__ import annotations
import pandas as pd
from core.demo_data import make_price_series


def load_market_data(symbol: str) -> pd.DataFrame:
    seed = abs(hash(symbol)) % (2**32)
    return make_price_series(seed=seed, periods=240)
