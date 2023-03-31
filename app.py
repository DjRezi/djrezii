import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the budget data
df_budget = pd.read_csv("budget_data.csv")

# Load the S&P 500 data
df_sp500 = pd.read_csv("sp500_data.csv")

# Set page title
st.set_page_config(page_title="Finance App", page_icon=":money_with_wings:")

# Set sidebar options
option = st.sidebar.selectbox('Select an Option', ('Homepage', 'Budget Analysis', 'S&P 500 Analysis'))

# Define function to format currency
def format_currency(amount):
    return '${:,.2f}'.format(amount)

# Define function to format percentage
def format_percentage(amount):
    return '{:.2f}%'.format(amount)

# Define function to calculate CAGR
def cagr(dataframe):
    start_value = dataframe.iloc[0]['Adj Close']
    end_value = dataframe.iloc[-1]['Adj Close']
    num_years = len(dataframe) / 252
    return ((end_value / start_value) ** (1 / num_years)) - 1

if option == 'Homepage':

    # Set page title
    st.title("Finance App")

    # Set page subtitle
    st.write("Welcome to the Finance App! This app provides analysis of personal finance and the stock market.")

    # Display image
    st.image("https://cdn.pixabay.com/photo/2016/02/19/11/19/stock-exchange-1215676_1280.jpg", use_column_width=True)

elif option == 'Budget Analysis':

    # Set page title
    st.title("Budget Analysis")

    # Display budget data
    st.write("### Monthly Budget Data")
    st.write(df_budget.style.format({"Income": format_currency, "Expenses": format_currency}))

    # Calculate net income and display
    net_income = df_budget["Income"].sum() - df_budget["Expenses"].sum()
    st.write("### Net Income")
    st.write(format_currency(net_income))

    # Calculate expense breakdown and display
    st.write("### Expense Breakdown")
    expense_breakdown = df_budget.groupby("Category")["Expenses"].sum().reset_index().sort_values(by="Expenses", ascending=False)
    expense_breakdown["% of Total"] = expense_breakdown["Expenses"] / df_budget["Expenses"].sum()
    expense_breakdown = expense_breakdown.style.format({"Expenses": format_currency, "% of Total": format_percentage})
    st.write(expense_breakdown)

elif option == 'S&P 500 Analysis':

    # Set page title
    st.title("S&P 500 Analysis")

    # Display S&P 500 data
    st.write("### S&P 500 Data")
    st.write(df_sp500)

    # Calculate and display CAGR
    cagr_value = cagr(df_sp500)
    st.write("### CAGR")
    st.write(format_percentage(cagr_value))

    # Calculate and display annualized standard deviation
    annualized_std_dev = np.std(df_sp500["Adj Close"].pct_change().dropna()) * np.sqrt(252)
    st.write("### Annualized Standard Deviation")
    st.write(format_percentage(annualized_std_dev))

    # Create histogram of daily returns
    daily_returns = df_sp500["Adj Close"].pct_change().dropna()
    fig, ax = plt.subplots()
    sns.histplot(data=daily_returns, ax=ax)
    ax.set
