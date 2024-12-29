import streamlit as st
import numpy as np
import pandas as pd
from models.BS_Model_Call import BS_Call, generate_and_plot_call_prices
from models.BS_Model_Put import BS_Put, generate_and_plot_put_prices
from models.Profit_or_Loss import plot_profit_or_loss_heatmap

st.set_page_config(layout="wide")

# Header
st.markdown("""# Black-Scholes Pricing Model""")

# Sidebar for Option Pricing Parameters
st.sidebar.header("Option Pricing Parameters")
st.sidebar.markdown("---")

# Input fields for option pricing parameters
S_0 = st.sidebar.number_input("Initial Spot Price", value=100.0, step=1.0)
K = st.sidebar.number_input("Strike Price", value=100.0, step=1.0)
r = st.sidebar.number_input("Risk-Free Rate", value=0.05, step=0.01)
time = st.sidebar.number_input("Time to Expiration", value=1.0, step=0.1)
sigma = st.sidebar.number_input("Annual Volatility", value=0.2, step=0.01)

# Sidebar for Heatmap Parameters
st.sidebar.header("Heatmap Parameters")
st.sidebar.markdown("---")

# Spot Price Range Slider
min_spot, max_spot = st.sidebar.slider(
    "Select Spot Price Range",
    min_value=50, 
    max_value=200, 
    value=(50, 150),
    step=1
)

# Volatility Range Slider
min_volatility, max_volatility = st.sidebar.slider(
    "Select Volatility Range",
    min_value=0.1,
    max_value=1.0,
    value=(0.2, 0.6),
    step=0.01
)

# Number of Points for Heatmap input
num_points = st.sidebar.number_input(
    "Number of Points for Heatmap", 
    min_value=5, 
    max_value=50, 
    value=10, 
    step=1
)

st.sidebar.markdown("---")

# Input fields for user-purchased option and type
st.sidebar.header("Your Option Purchase")
option_type = st.sidebar.selectbox("Select Option Type", ["Call", "Put"])
purchase_price = st.sidebar.number_input("Enter Your Purchase Price ($)", value=10.0, step=0.1)

st.sidebar.markdown("---")

# Display the entered option parameters
st.write("### Option Features")
data = {
    "Initial Spot Price": [S_0],
    "Strike Price": [K],
    "Risk-Free Rate": [r],
    "Time to Expiration": [time],
    "Volatility": [sigma],
}
st.table(data)

# Calculate Call and Put Prices
call_price = BS_Call(S_0, K, time, r, sigma)
put_price = BS_Put(S_0, K, time, r, sigma)

# Display Call and Put Prices in styled boxes
st.markdown(f"""
    <div style="display: flex; justify-content: space-between;">
        <div style="background-color: #d4edda; padding: 10px 20px; border-radius: 10px; width: 45%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; height: 120px;">
            <h4 style="color: #6c757d; margin-bottom: 0px;">Call Price</h4>
            <h3 style="color: green; font-size: 40px; margin-top: 0px;">${call_price:.2f}</h3>
        </div>
        <div style="background-color: #f8d7da; padding: 10px 20px; border-radius: 10px; width: 45%; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; height: 120px;">
            <h4 style="color: #6c757d; margin-bottom: 0px;">Put Price</h4>
            <h3 style="color: red; font-size: 40px; margin-top: 0px;">${put_price:.2f}</h3>
        </div>
    </div>
""", unsafe_allow_html=True)

# Add extra space after the price boxes for better readability
st.markdown("<br><br>", unsafe_allow_html=True)

# Interactive Heatmap Header
st.markdown("### Option Price - Interactive Heatmap")

# Concise description of the heatmap
st.write(
    "Explore how **call** and **put** option prices change with varying spot prices and volatilities. "
    "Adjust the sliders to see the impact on option prices."
)

# Add extra space after the heatmap description
st.markdown("<br>", unsafe_allow_html=True)

# Display Heatmaps side by side
col1, col2 = st.columns(2)

# Call Price Heatmap
with col1:
    st.write("#### Call Price Heatmap")
    calls_df, call_heatmap = generate_and_plot_call_prices(S_0, sigma, K, time, r, min_spot, max_spot, min_volatility, max_volatility, num_points)
    st.pyplot(call_heatmap.figure)

# Add extra space after the call price heatmap
st.markdown("<br>", unsafe_allow_html=True)

# Put Price Heatmap
with col2:
    st.write("#### Put Price Heatmap")
    puts_df, put_heatmap = generate_and_plot_put_prices(S_0, sigma, K, time, r, min_spot, max_spot, min_volatility, max_volatility, num_points)
    st.pyplot(put_heatmap.figure)

# Add extra space after the put price heatmap
st.markdown("<br><br>", unsafe_allow_html=True)

# Call the plot_profit_or_loss_heatmap function based on user's choice of option type
if option_type == "Call":
    # Calculate the PnL for call option purchase
    st.write("### Theoretical Profit or Loss for Your Purchased Call Option")
    
    # Description for the heatmap
    st.write(
        "This heatmap shows the theoretical **profit or loss** for your purchased **call option**. "
        "The color scale indicates how the option's value changes based on variations in spot price and volatility. "
        "Green represents profitable regions, while red indicates potential losses."
    )
    
    call_option_prices = calls_df.values  # Use the generated call option prices
    market_prices = np.full_like(call_option_prices, purchase_price)  # User's purchase price
    pnl_df, pnl_heatmap = plot_profit_or_loss_heatmap(call_option_prices, market_prices, np.linspace(min_spot, max_spot, num_points), np.linspace(min_volatility, max_volatility, num_points), option_type="call")
    st.pyplot(pnl_heatmap.figure)

    # Add space after the PnL heatmap
    st.markdown("<br>", unsafe_allow_html=True)

    # Calculate profit or loss from the user's purchase price
    profit_or_loss = call_price - purchase_price

elif option_type == "Put":
    # Calculate the PnL for put option purchase
    st.write("### Theoretical Profit or Loss for Your Purchased Put Option")
    
    # Description for the heatmap
    st.write(
        "This heatmap shows the theoretical **profit or loss** for your purchased **put option**. "
        "The color scale indicates how the option's value changes based on variations in spot price and volatility. "
        "Green represents profitable regions, while red indicates potential losses."
    )
    
    put_option_prices = puts_df.values  # Use the generated put option prices
    market_prices = np.full_like(put_option_prices, purchase_price)  # User's purchase price
    pnl_df, pnl_heatmap = plot_profit_or_loss_heatmap(put_option_prices, market_prices, np.linspace(min_spot, max_spot, num_points), np.linspace(min_volatility, max_volatility, num_points), option_type="put")
    st.pyplot(pnl_heatmap.figure)

    # Add space after the PnL heatmap
    st.markdown("<br>", unsafe_allow_html=True)

    # Calculate profit or loss from the user's purchase price
    profit_or_loss = put_price - purchase_price

# Display profit or loss in the bottom part of the page
if profit_or_loss > 0:
    st.markdown(f'<p style="color: green;">You made a profit of ${profit_or_loss:.2f} on your investment!</p>', unsafe_allow_html=True)
elif profit_or_loss < 0:
    st.markdown(f'<p style="color: red;">You made a loss of ${abs(profit_or_loss):.2f} on your investment.</p>', unsafe_allow_html=True)
else:
    st.markdown('<p style="color: gray;">Your investment has broken even.</p>', unsafe_allow_html=True)
