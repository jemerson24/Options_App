import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# Define the cumulative distribution formula for Black-Scholes Call
N = norm.cdf

# Black-Scholes Call Formula Function
def BS_Call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * N(d1) - K * np.exp(-r * T) * N(d2)

# Wrapper function to compute and return a single call price
def get_call_price(S_0, K, time, r, sigma):
    return BS_Call(S_0, K, time, r, sigma)

# Generate and plot call prices with new min/max for spot price and volatility
def generate_and_plot_call_prices(S_0, sigma, K, time, r, min_spot, max_spot, min_volatility, max_volatility, num_points=10):
    # Generate ranges for spot prices and volatilities based on the provided min/max values
    spot_prices = np.linspace(min_spot, max_spot, num_points)  # Range between min and max spot prices
    volatilities = np.linspace(min_volatility, max_volatility, num_points)  # Range between min and max volatilities

    # Create a 2D array for call prices
    call_prices = np.zeros((len(volatilities), len(spot_prices)))

    # Compute call prices using the Black-Scholes model
    for i, vol in enumerate(volatilities):
        for j, spot in enumerate(spot_prices):
            call_prices[i, j] = BS_Call(spot, K, time, r, vol)
    
    # Plot the heatmap using seaborn with red-to-green color map
    plt.figure(figsize=(10, 8))
    call_heatmap = sns.heatmap(call_prices, 
                               xticklabels=np.round(spot_prices, 2), 
                               yticklabels=np.round(volatilities, 2), 
                               cmap='RdYlGn', cbar_kws={'label': 'Call Price'},
                               annot=True, fmt=".2f")  # Show values in each cell
    plt.title('Black-Scholes Call Price Matrix')
    plt.xlabel('Spot Price')
    plt.ylabel('Volatility')
    plt.show()

    # Create and return DataFrame of the call prices
    calls_df = pd.DataFrame(call_prices, columns=np.round(spot_prices, 2), index=np.round(volatilities, 2))
    
    return calls_df, call_heatmap
