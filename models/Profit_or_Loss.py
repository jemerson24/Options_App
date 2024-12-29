import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def plot_profit_or_loss_heatmap(option_prices, market_prices, spot_prices, volatilities, option_type="call"):
    # Ensure market_prices is converted to a NumPy array if necessary
    market_prices = np.array(market_prices)

    # Compute profit or loss
    pnl = option_prices - market_prices

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    pnl_heatmap = sns.heatmap(pnl, 
                              xticklabels=np.round(spot_prices, 2), 
                              yticklabels=np.round(volatilities, 2), 
                              cmap='RdYlGn',  # Green for positive, red for negative
                              cbar_kws={'label': 'Profit / Loss ($)'},
                              annot=True, fmt=".2f")  # Show values in each cell
    plt.title(f'Profit and Loss Heatmap for {option_type.capitalize()} Options')
    plt.xlabel('Spot Price')
    plt.ylabel('Volatility')
    plt.show()

    # Create and return a DataFrame of the profit or loss
    pnl_df = pd.DataFrame(pnl, columns=np.round(spot_prices, 2), index=np.round(volatilities, 2))
    return pnl_df, pnl_heatmap