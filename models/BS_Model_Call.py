import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# #Define Variables

# S_0 = 100  # Initial spot price
# K = 100  # Strike price
# r = 0.1  # Risk-free rate
# time = 1  # Time until option expiration
# sigma = 0.3  # Annual volatility of asset's return

# Define the cumulative distribution formula for Black-Scholes Call
N = norm.cdf

# Black-Scholes Call Formula Function
def BS_Call(S, K, T, r, sigma):
    # d1 adjusts for expected stock price if option is exercised
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    # d2 is probability the option will expire in the money
    d2 = d1 - sigma * np.sqrt(T)
    # BS Call Formula no dividends
    return S * N(d1) - K * np.exp(-r * T) * N(d2)

# Wrapper function to compute and return a single call price
def get_call_price(S_0, K, time, r, sigma):
    return BS_Call(S_0, K, time, r, sigma)

# Generate and plot call prices
def generate_and_plot_call_prices(S_0, sigma, K, time, r, spot_range=50, volatility_range=0.1, num_points=10):
    # Generate ranges for spot prices and volatilities
    spot_prices = np.linspace(S_0 - spot_range, S_0 + spot_range, num_points)  # Range around S_0
    volatilities = np.linspace(sigma - volatility_range, sigma + volatility_range, num_points)  # Range around sigma

    # Create a 2D array for call prices
    call_prices = np.zeros((len(volatilities), len(spot_prices)))

    # Compute call prices using the Black-Scholes model
    for i, vol in enumerate(volatilities):
        for j, spot in enumerate(spot_prices):
            call_prices[i, j] = BS_Call(spot, K, time, r, vol)
    
    # Plot the heatmap using seaborn
    plt.figure(figsize=(10, 8))
    call_heatmap = sns.heatmap(call_prices, 
                               xticklabels=np.round(spot_prices, 2), 
                               yticklabels=np.round(volatilities, 2), 
                               cmap='viridis', cbar_kws={'label': 'Call Price'},
                               annot=True, fmt=".2f")  # Show values in each cell
    plt.title('Black-Scholes Call Price Matrix')
    plt.xlabel('Spot Price')
    plt.ylabel('Volatility')
    plt.show()

    # Create and return DataFrame of the call prices
    calls_df = pd.DataFrame(call_prices, columns=np.round(spot_prices, 2), index=np.round(volatilities, 2))
    
    return calls_df, call_heatmap
