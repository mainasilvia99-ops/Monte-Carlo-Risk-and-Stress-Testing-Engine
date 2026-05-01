# Monte-Carlo-Risk-and-Stress-Testing-Engine

#  Monte Carlo Simulation for Portfolio Risk & Stress Testing 

This project implements a multi-asset Monte Carlo simulation framework to model portfolio risk under realistic financial conditions.

---

##  Overview

Traditional financial models assume normally distributed returns. This project extends beyond that by incorporating:

- Correlated asset simulation (Cholesky decomposition)
- Gaussian mixture models (fat tails & regime shifts)
- Merton jump-diffusion (market crashes)
- Portfolio aggregation and tail-risk metrics

---

##  Models Implemented

### 1. Geometric Brownian Motion (GBM)
Baseline continuous-time model.

### 2. Gaussian Mixture Model
Captures:
- skewness
- heavy tails
- regime switching

### 3. Merton Jump-Diffusion
Captures:
- discontinuities
- crash dynamics
- extreme downside risk

---

##  Risk Metrics

- Value at Risk (VaR)
- Expected Shortfall (ES)

---

##  Key Results

### Distribution Characteristics (Mixture Model)
- Mean: -0.00408  
- Std Dev: 0.02191  
- Skewness: -2.80 (strong left tail)  
- Excess Kurtosis: 10.75 (fat tails)

 Indicates significant downside risk and deviation from normality.

---

### Correlation Validation

Target vs simulated correlations:

| Pair | Target | Simulated |
|------|--------|-----------|
| 1–2  | 0.50   | 0.5047    |
| 1–3  | 0.30   | 0.3016    |
| 2–3  | 0.40   | 0.4043    |

Confirms accurate Cholesky implementation.

---

### GBM Validation

- Simulated: 51.94  
- Theoretical: 52.04  

 Monte Carlo converges to analytical expectation.

---

### Risk Comparison Across Models

| Model    | VaR (95%) | ES |
|----------|----------|------|
| Normal   | -0.0330  | -0.0413 |
| Mixture  | -0.0499  | -0.0814 |
| Jump     | -0.4264  | -0.5339 |

---

##  Key Insights

1. **Normal models severely underestimate risk**
   - Lowest VaR and ES
   - Thin tails

2. **Mixture models capture real-world asymmetry**
   - Negative skewness
   - fat tails

3. **Jump diffusion dramatically increases tail risk**
   - Extreme losses appear
   - most realistic crisis behavior

4. **Correlation modelling is critical**
   - accurately reproduced via Cholesky decomposition

---

##  Concepts Applied

- Monte Carlo simulation
- Random variate generation
- Cholesky decomposition
- Stochastic processes (GBM, Jump diffusion)
- Risk metrics (VaR, Expected Shortfall)

---

##  Future Work

- Option pricing via Monte Carlo
- Variance reduction techniques
- Real market calibration
- Backtesting VaR accuracy

---
Built as part of computational finance and financial engineering training.

##  Author
Maina Silvia
