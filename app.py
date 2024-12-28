import streamlit as st

import numpy as np
import pandas as pd
from models.BS_Model_Call import BS_Call, get_call_price, generate_and_plot_call_prices
from models.BS_Model_Put import BS_Put, get_put_price, generate_and_plot_put_prices


st.markdown("""# Black-Scholes Pricing Model""")

# Sidebar inputs
st.sidebar.header("Option Pricing Parameters")

S_0 = st.sidebar.number_input("Initial Spot Price (S_0)", value=100.0, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0, step=1.0)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.1, step=0.01)
time = st.sidebar.number_input("Time to Expiration (time)", value=1.0, step=0.1)
sigma = st.sidebar.number_input("Annual Volatility (sigma)", value=0.3, step=0.01)


# Display the entered values in the main app area
st.write("### Option Features")

# Create a table with parameter names as column labels
data = {
    "Initial Spot Price (S_0)": [S_0],
    "Strike Price (K)": [K],
    "Risk-Free Rate (r)": [r],
    "Time to Expiration (time)": [time],
    "Annual Volatility (sigma)": [sigma]
}
st.table(data)

# Calculate BS Call and Put prices
call_price = BS_Call(S_0, K, time, r, sigma)
put_price = BS_Put(S_0, K, time, r, sigma)

# Display the results in green and red boxes
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






