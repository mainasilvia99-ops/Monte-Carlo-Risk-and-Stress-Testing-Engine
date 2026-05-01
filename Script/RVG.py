# ==========================================================
# COMPUTATIONAL FINANCE NOTEBOOK
# Random Variate Generation, Monte Carlo, Correlation, Jumps
# ==========================================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, weibull_min, binom, skew, kurtosis

np.random.seed(42)

# ==========================================
# 1. INVERSE TRANSFORM - WEIBULL
# ==========================================
N = 5000
k, lam = 2, 3
U = np.random.uniform(0,1,N)
X = lam * (-np.log(1-U))**(1/k)

x = np.linspace(0,10,100)
plt.hist(X, bins=50, density=True, alpha=0.6)
plt.plot(x, weibull_min.pdf(x, k, scale=lam))
plt.title("Weibull Distribution (Inverse Transform)")
plt.show()

# ==========================================
# 2. BOX-MULLER (NORMAL GENERATION)
# ==========================================
N = 50000
U1 = np.random.uniform(0,1,N)
U2 = np.random.uniform(0,1,N)

Z1 = np.sqrt(-2*np.log(U1))*np.cos(2*np.pi*U2)
Z2 = np.sqrt(-2*np.log(U1))*np.sin(2*np.pi*U2)

plt.hist(Z1, bins=100, density=True)
plt.title("Standard Normal via Box-Muller")
plt.show()

# ==========================================
# 3. GAUSSIAN MIXTURE
# ==========================================
N = 200000
U = np.random.uniform(0,1,N)

X = np.where(U < 0.9,
             np.random.normal(0.001, 0.01, N),
             np.random.normal(-0.05, 0.04, N))

print("Mean:", np.mean(X))
print("Std:", np.std(X))
print("Skew:", skew(X))
print("Kurtosis:", kurtosis(X))

plt.hist(X, bins=100, density=True)
plt.title("Gaussian Mixture")
plt.show()

# ==========================================
# 4. CHOLESKY - CORRELATED ASSETS
# ==========================================
sigma = np.array([0.2,0.25,0.3])
corr = np.array([
    [1,0.5,0.3],
    [0.5,1,0.4],
    [0.3,0.4,1]
])

Sigma = np.outer(sigma,sigma)*corr
L = np.linalg.cholesky(Sigma)

Z = np.random.normal(size=(100000,3))
X_corr = Z @ L.T

print("Sample Correlation:\n", np.corrcoef(X_corr.T))

plt.scatter(X_corr[:,0], X_corr[:,1], alpha=0.3)
plt.title("Correlated Assets")
plt.show()

# ==========================================
# 5. GBM SIMULATION
# ==========================================
S0, mu, sigma, T = 50, 0.08, 0.25, 0.5
N = 50000
Z = np.random.normal(0,1,N)

ST = S0*np.exp((mu-0.5*sigma**2)*T + sigma*np.sqrt(T)*Z)

print("E[ST] sim:", np.mean(ST))
print("E[ST] exact:", S0*np.exp(mu*T))

plt.hist(ST, bins=100)
plt.title("GBM Terminal Prices")
plt.show()

# ==========================================
# 6. MERTON JUMP DIFFUSION
# ==========================================
N = 20000
T = 252
mu = 0.08/252
sigma = 0.25/np.sqrt(252)
lam = 3/252
muJ, sigmaJ = -0.03, 0.02

annual_returns = []

for i in range(N):
    r_sum = 0
    for t in range(T):
        Z = np.random.normal()
        jumps = np.random.poisson(lam)
        J = np.sum(np.random.normal(muJ, sigmaJ, jumps))
        r_sum += mu + sigma*Z + J
    annual_returns.append(r_sum)

annual_returns = np.array(annual_returns)

plt.hist(annual_returns, bins=100, density=True)
plt.title("Jump Diffusion Returns")
plt.show()

print("Skew:", skew(annual_returns))
print("Kurtosis:", kurtosis(annual_returns))

##OUTPUTS
# ( Mean: -0.00408173680256779
#Std: 0.02191161901311222
#Skew: -2.8001281866756127
#Kurtosis: 10.750026369641468
#Sample Correlation:
#[[1.         0.50465731 0.30157293]
# [0.50465731 1.         0.40426928]
# [0.30157293 0.40426928 1.        ]]
#E[ST] sim: 51.94246573154758
#E[ST] exact: 52.04053870961941
#Skew: -0.007975307881001257
#Kurtosis: 0.0034760546375305346)

#--- PORTFOLIO SETUP ---
# Portfolio weights
import numpy as np
w = np.array([0.4, 0.35, 0.25])

# Simulated correlated returns (reuse from earlier)
returns = X_corr  # from Cholesky step

# Portfolio returns
portfolio_returns = returns @ w

# --- VaR & Expected Shortfall ---
def compute_var_es(data, alpha=0.95):
    var = np.percentile(data, (1-alpha)*100)
    es = data[data <= var].mean()
    return var, es

var, es = compute_var_es(portfolio_returns)

print("VaR (95%):", var)
print("Expected Shortfall:", es)

# --- COMPARING MODELS ---
# Normal model
normal_returns = np.random.normal(0, 0.02, 100000)

# Mixture model (reuse earlier)
mixture_returns = X

# Jump model (reuse annual_returns)
jump_returns = annual_returns

# Plot comparison
plt.hist(normal_returns, bins=100, alpha=0.4, label="Normal", density=True)
plt.hist(mixture_returns, bins=100, alpha=0.4, label="Mixture", density=True)
plt.hist(jump_returns, bins=100, alpha=0.4, label="Jump", density=True)

plt.legend()
plt.title("Return Distributions Comparison")
plt.show()


#--- TAIL COMPARISON ---
for name, data in zip(
    ["Normal", "Mixture", "Jump"],
    [normal_returns, mixture_returns, jump_returns]
):
    var, es = compute_var_es(data)
    print(name, "VaR:", var, "ES:", es)



# ==========================================
# END
# ==========================================
