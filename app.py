import streamlit as st
import pandas as pd
import altair as alt

# Load data
df_budget = pd.read_csv("https://raw.githubusercontent.com/djrezii/Streamlit-Finance-App/master/data/budget_data.csv")
df_spending = pd.read_csv("https://raw.githubusercontent.com/djrezii/Streamlit-Finance-App/master/data/spending_data.csv")
df_income = pd.read_csv("https://raw.githubusercontent.com/djrezii/Streamlit-Finance-App/master/data/income_data.csv")

# Combine budget and spending data
df_budget_spending = pd.merge(df_budget, df_spending, on="Category")

# Calculate remaining budget
df_budget_spending["Remaining"] = df_budget_spending["Budget"] - df_budget_spending["Spending"]

# Set page title
st.set_page_config(page_title="Personal Finance Management")

# Set app title
st.title("Personal Finance Management")

# Add subheader for budget
st.subheader("Budget Overview")

# Display budget table
st.write(df_budget)

# Create a chart of budget vs spending
chart_data = df_budget_spending[["Category", "Budget", "Spending"]].set_index("Category").stack().reset_index()
chart_data.columns = ["Category", "Budget/Spending", "Amount"]
chart = alt.Chart(chart_data).mark_bar().encode(
    x="Category",
    y="Amount",
    color="Budget/Spending"
)
st.altair_chart(chart, use_container_width=True)

# Add subheader for income and spending
st.subheader("Income and Spending Overview")

# Display income and spending table
st.write(df_income)
st.write(df_spending)

# Create a chart of income vs spending
income_spending_data = pd.concat([df_income, df_spending])
chart_data = income_spending_data[["Category", "Amount", "Type"]].set_index("Category").stack().reset_index()
chart_data.columns = ["Category", "Type", "Amount"]
chart = alt.Chart(chart_data).mark_bar().encode(
    x="Category",
    y="Amount",
    color="Type"
)
st.altair_chart(chart, use_container_width=True)

# Add subheader for remaining budget
st.subheader("Remaining Budget by Category")

# Display remaining budget table
st.write(df_budget_spending[["Category", "Remaining"]])
