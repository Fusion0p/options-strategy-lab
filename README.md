# Options Strategy Lab

A personal project born out of genuine obsession with options markets — built to understand derivatives not just in theory, but by reconstructing the mechanics from the ground up.

This is a full-stack quantitative research platform for backtesting and simulating NSE options strategies, with a live-market-style interactive interface. Every component — the Greeks engine, the signal system, the Monte Carlo simulator — was built from scratch.

---

## Why I Built This

I started trading options a couple of years ago and quickly realised that most retail tools give you outcomes without giving you understanding. I wanted to know *why* an Iron Condor loses money when volatility spikes, *how* theta decay accelerates near expiry, and *what* a portfolio's real risk profile looks like across thousands of possible market paths — not just in the one path that history gave us.

So I built the tool I wished existed.

---

## What It Does

### Options Strategy Backtester
Test 6+ major options strategies on historical NSE data with execution realism built in:
- **Strategies supported:** Iron Condor, Short Strangle, Straddle, Bull Call Spread, Bear Put Spread, Covered Call
- **Execution modelling:** transaction costs, slippage, and bid-ask spread simulation — not just clean theoretical fills
- **Performance analytics:** Sharpe ratio, Sortino ratio, Calmar ratio, Maximum Drawdown, Win Rate, and regime-wise comparison against NIFTY benchmark

### Greeks Engine
A complete from-scratch implementation of the Black-Scholes Greeks at both position and portfolio level:
- **Delta** — directional exposure
- **Gamma** — rate of change of delta
- **Theta** — time decay
- **Vega** — volatility sensitivity
- **Rho** — interest rate sensitivity
- **Portfolio-level aggregation** — see your net Greeks across an entire multi-leg position
- **VaR calculation** and historical stress testing

### Manual Trade Simulator
The part I found most useful for developing market intuition:
- Replay any historical period candle by candle
- Enter and exit positions at any point
- See instant P&L, Greeks exposure, and return attribution updated in real time
- Understand how a position behaves as time passes and spot moves — not just at expiry

### Multi-Factor Signal Engine
Combines three categories of input to generate trade signals:
- **Technical indicators** — 11 indicators covering momentum, trend, and volume
- **Volatility regime detection** — classifies market as bull, bear, or sideways to assess whether a strategy is appropriate for current conditions
- **NLP news sentiment** — scores financial news headlines and integrates sentiment as a signal input

Signals come with a confidence score and plain-language explanation — not just buy/sell/hold.

### Robustness Testing
- **Walk-forward optimisation** — avoids overfitting by testing parameter stability across out-of-sample periods
- **Monte Carlo simulation** — 10,000 paths using Geometric Brownian Motion to generate a distribution of outcomes rather than a single backtest result
- **Parameter sensitivity analysis** — understand how much your results depend on specific parameter choices

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Data manipulation | Pandas, NumPy |
| Options pricing | Black-Scholes (custom implementation) |
| Machine learning | Scikit-Learn |
| Sentiment analysis | NLP pipeline |
| Visualisation | Plotly |
| Interface | Streamlit |

---

## Project Structure

```
options-strategy-lab/
│
├── options-strategy-lab/
│   ├── strategies/          # Strategy definitions and payoff logic
│   ├── greeks/              # Greeks engine — Black-Scholes implementation
│   ├── backtester/          # Core backtesting engine
│   ├── simulator/           # Manual trade simulator
│   ├── signals/             # Multi-factor signal engine
│   ├── sentiment/           # NLP news sentiment pipeline
│   ├── montecarlo/          # Monte Carlo simulation module
│   ├── analytics/           # Performance metrics and reporting
│   └── app.py               # Streamlit application entry point
```

---

## Getting Started

**Clone the repository:**
```bash
git clone https://github.com/Fusion0p/options-strategy-lab.git
cd options-strategy-lab
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run the app:**
```bash
streamlit run app.py
```

---

## Key Concepts Implemented

**Black-Scholes Pricing**
Options are priced using the Black-Scholes model with the full set of Greeks computed analytically. The implementation assumes European-style exercise — relevant for NSE index options.

**Walk-Forward Optimisation**
Rather than optimising parameters on the full dataset (which leads to overfitting), the backtester uses walk-forward windows: optimise on a training window, test on the following out-of-sample window, roll forward, repeat. This gives a more realistic picture of how a strategy would have actually performed.

**Monte Carlo via GBM**
Price paths are simulated using Geometric Brownian Motion:

```
S(t) = S(0) * exp((μ - σ²/2)*t + σ*√t*Z)
```

where Z is drawn from a standard normal distribution. Running 10,000 paths gives a stable distribution of strategy outcomes and allows estimation of tail risk.

**Volatility Regime Detection**
Before applying any strategy, the system classifies current market conditions using a combination of realised volatility, trend strength, and volume metrics. Certain strategies (like short strangles) are only appropriate in low-volatility sideways regimes — the signal engine accounts for this.

---

## Limitations and Honest Caveats

- **Data:** Built on NSE historical data. Results do not generalise directly to international markets without recalibration
- **Black-Scholes assumptions:** The model assumes constant volatility — a known oversimplification. Real markets exhibit volatility smiles and skew
- **Execution:** Slippage and transaction cost estimates are approximations. Actual execution in live markets would differ
- **Sentiment lag:** News-based sentiment signals have inherent lag — prices often move before news is published

These limitations are not bugs — they are the reason the robustness testing modules exist.

---

## What I Learned Building This

The Greeks engine taught me more about options than any course. When you implement Gamma from the formula yourself and watch it spike as expiry approaches for an ATM option, it stops being a definition and becomes an intuition. Same with Theta — building the day-by-day decay calculation makes the acceleration near expiry viscerally clear.

The Monte Carlo module changed how I think about backtesting entirely. A single backtest is one path through one universe. Ten thousand simulated paths show you the distribution of what *could* have happened — which is a much more honest picture of a strategy's true robustness.

---

## Related Project

[Multi-Factor Market Intelligence & Backtesting System](https://github.com/Fusion0p/Multi-Factor-Market-Intelligence-) — a quantitative signal engine combining price momentum, volume, and NLP sentiment to generate explainable trade signals with regime-based classification.

---

## Author

**Shrey Bhardwaj**
[LinkedIn](https://www.linkedin.com/in/shrey-bhardwaj-999962262/) · [GitHub](https://github.com/Fusion0p)

NISM Series VIII & I Certified · CFA Level 1 Candidate

---

*Built out of curiosity. Every line written to understand markets better, not just to pass a course.*
