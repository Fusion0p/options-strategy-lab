from __future__ import annotations
import numpy as np


def var_es(returns, level: float = 0.95):
    arr = np.asarray(returns)
    q = np.quantile(arr, 1-level)
    es = arr[arr <= q].mean() if np.any(arr <= q) else q
    return float(q), float(es)
