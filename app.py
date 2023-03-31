import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load data
df_portfolio = pd.DataFrame({
    'Asset': ['AAPL', 'AMZN', 'GOOG', 'NFLX', 'TSLA'],
    'Allocation': [20, 20, 20, 20, 20]
})

df_budget = pd.DataFrame({
    'Category': ['Housing', 'Transportation', 'Food', 'Utilities', 'Entertainment', 'Other'],
    'Budgeted_Amount': [1500, 500, 800, 350, 200, 400]
})

df_sp500 = pd.read_csv("sp500_data.csv")

# Sidebar
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose the app mode", ["Homepage", "Portfolio", "Budget", "S&P 500"])

# Main app
st.title("Finance App")

if app_mode == "Homepage":
    st.write("Welcome to the Finance App! Please select a page on the sidebar.")
    
elif app_mode == "Portfolio":
    st.subheader("Portfolio Allocation")
    st.write(df_portfolio)

    fig = px.pie(df_portfolio, values='Allocation', names='Asset', title='Portfolio Allocation')
    st.plotly_chart(fig)
    
elif app_mode == "Budget":
    st.subheader("Monthly Budget")
    st.write(df_budget)

    fig = px.bar(df_budget, x='Category', y='Budgeted_Amount', title='Monthly Budget')
    st.plotly_chart(fig)
    
elif app_mode == "S&P 500":
    st.subheader("S&P 500 Data")
    st.write(df_sp500)

    fig = px.line(df_sp500, x='date', y='close', title='S&P 500 Closing Prices')
    st.plotly_chart(fig)
