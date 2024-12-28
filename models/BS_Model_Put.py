import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# # #Define Variables

# S_0 = 100  # Initial spot price
# K = 100  # Strike price
# r = 0.1  # Risk-free rate
# time = 1  # Time until option expiration
# sigma = 0.3  # Annual volatility of asset's return

#Define cumuliative distribution formula for BS_CALL and BS_PUT
N = norm.cdf

# Black-Scholes Put Formula Function
def BS_Put(S, K, T, r, sigma):
    # d1 adjusts for expected stock price if option is exercised
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    # d2 is probability the option will expire in the money
    d2 = d1 - sigma * np.sqrt(T)
    # BS Put Formula no dividends
    return K * np.exp(-r * T) * N(-d2) - S * N(-d1)

# Call Statement Example
# Put_est = BS_Put(S_0, K, time, r, sigma)

def generate_and_plot_put_prices(S_0, sigma, K, time, r, spot_range=50, volatility_range=0.1, num_points=10):
    # Generate ranges for spot prices and volatilities
    spot_prices = np.linspace(S_0 - spot_range, S_0 + spot_range, num_points)  # Range around S_0
    volatilities = np.linspace(sigma - volatility_range, sigma + volatility_range, num_points)  # Range around sigma

    # Create a 2D array for put prices
    put_prices = np.zeros((len(volatilities), len(spot_prices)))

    # Compute put prices using the Black-Scholes model
    for i, vol in enumerate(volatilities):
        for j, spot in enumerate(spot_prices):
            put_prices[i, j] = BS_Put(spot, K, time, r, vol)
    
    # Plot the heatmap using seaborn
    plt.figure(figsize=(10, 8))
    ax = sns.heatmap(put_prices, 
                     xticklabels=np.round(spot_prices, 2), 
                     yticklabels=np.round(volatilities, 2), 
                     cmap='viridis', cbar_kws={'label': 'Put Price'},
                     annot=True, fmt=".2f")  # Show values in each cell
    plt.title('Black-Scholes Put Price Matrix')
    plt.xlabel('Spot Price')
    plt.ylabel('Volatility')
    plt.show()

    # Create and return DataFrame of the put prices
    puts_df = pd.DataFrame(put_prices, columns=np.round(spot_prices, 2), index=np.round(volatilities, 2))
    
    return puts_df
