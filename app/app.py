import streamlit as st

import numpy as np
import pandas as pd

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

df = pd.DataFrame({
    'first column': list(range(1, 11)),
    'second column': np.arange(10, 101, 10)
})

# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider
line_count = st.slider('Select a line count', 1, 10, 3)

# and used to select the displayed lines
head_df = df.head(line_count)

head_df