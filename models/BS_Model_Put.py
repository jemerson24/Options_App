import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns

# Define the cumulative distribution formula for BS_Put
N = norm.cdf

# Black-Scholes Put Formula Function
def BS_Put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * N(-d2) - S * N(-d1)

# Wrapper function to compute and return a single put price
def get_put_price(S_0, K, time, r, sigma):
    return BS_Put(S_0, K, time, r, sigma)

# Generate and plot put prices with new min/max for spot price and volatility
def generate_and_plot_put_prices(S_0, sigma, K, time, r, min_spot, max_spot, min_volatility, max_volatility, num_points=10):
    # Generate ranges for spot prices and volatilities based on the provided min/max values
    spot_prices = np.linspace(min_spot, max_spot, num_points)  # Range between min and max spot prices
    volatilities = np.linspace(min_volatility, max_volatility, num_points)  # Range between min and max volatilities

    # Create a 2D array for put prices
    put_prices = np.zeros((len(volatilities), len(spot_prices)))

    # Compute put prices using the Black-Scholes model
    for i, vol in enumerate(volatilities):
        for j, spot in enumerate(spot_prices):
            put_prices[i, j] = BS_Put(spot, K, time, r, vol)
    
    # Plot the heatmap using seaborn with red-to-green color map
    plt.figure(figsize=(10, 8))
    put_heatmap = sns.heatmap(put_prices, 
                              xticklabels=np.round(spot_prices, 2), 
                              yticklabels=np.round(volatilities, 2), 
                              cmap='RdYlGn', cbar_kws={'label': 'Put Price'},
                              annot=True, fmt=".2f")  # Show values in each cell
    plt.title('Black-Scholes Put Price Matrix')
    plt.xlabel('Spot Price')
    plt.ylabel('Volatility')
    plt.show()

    # Create and return DataFrame of the put prices
    puts_df = pd.DataFrame(put_prices, columns=np.round(spot_prices, 2), index=np.round(volatilities, 2))
    
    return puts_df, put_heatmap
