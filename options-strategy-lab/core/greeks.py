from __future__ import annotations
import math
from dataclasses import dataclass


def _norm_pdf(x: float) -> float:
    return math.exp(-0.5 * x * x) / math.sqrt(2 * math.pi)


def _norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


@dataclass
class GreeksResult:
    price: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float


def black_scholes_greeks(spot: float, strike: float, time_to_expiry: float, rate: float, vol: float, option_type: str = "call") -> GreeksResult:
    if time_to_expiry <= 0 or vol <= 0 or spot <= 0 or strike <= 0:
        intrinsic = max(spot - strike, 0.0) if option_type == "call" else max(strike - spot, 0.0)
        return GreeksResult(intrinsic, 0.0, 0.0, 0.0, 0.0, 0.0)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol ** 2) * time_to_expiry) / (vol * math.sqrt(time_to_expiry))
    d2 = d1 - vol * math.sqrt(time_to_expiry)
    if option_type == "call":
        price = spot * _norm_cdf(d1) - strike * math.exp(-rate * time_to_expiry) * _norm_cdf(d2)
        delta = _norm_cdf(d1)
        theta = (-(spot * _norm_pdf(d1) * vol) / (2 * math.sqrt(time_to_expiry)) - rate * strike * math.exp(-rate * time_to_expiry) * _norm_cdf(d2)) / 365
        rho = strike * time_to_expiry * math.exp(-rate * time_to_expiry) * _norm_cdf(d2) / 100
    else:
        price = strike * math.exp(-rate * time_to_expiry) * _norm_cdf(-d2) - spot * _norm_cdf(-d1)
        delta = _norm_cdf(d1) - 1
        theta = (-(spot * _norm_pdf(d1) * vol) / (2 * math.sqrt(time_to_expiry)) + rate * strike * math.exp(-rate * time_to_expiry) * _norm_cdf(-d2)) / 365
        rho = -strike * time_to_expiry * math.exp(-rate * time_to_expiry) * _norm_cdf(-d2) / 100
    gamma = _norm_pdf(d1) / (spot * vol * math.sqrt(time_to_expiry))
    vega = spot * _norm_pdf(d1) * math.sqrt(time_to_expiry) / 100
    return GreeksResult(price, delta, gamma, theta, vega, rho)
