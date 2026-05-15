from __future__ import annotations
import io
import pandas as pd


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode('utf-8')


def summary_text(metrics: dict) -> str:
    return "\n".join([f"{k}: {v}" for k, v in metrics.items()])
