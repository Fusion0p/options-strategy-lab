from __future__ import annotations
import pandas as pd


def sentiment_score(news: pd.DataFrame) -> float:
    if news.empty or 'sentiment' not in news.columns:
        return 0.0
    return float(news['sentiment'].mean())
