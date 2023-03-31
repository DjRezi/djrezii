import streamlit as st
import pandas as pd
import altair as alt

# Define the datasets
spending_categories = {
    'Housing': 0.3,
    'Transportation': 0.15,
    'Food': 0.1,
    'Utilities': 0.1,
    'Insurance': 0.05,
    'Medical': 0.05,
    'Savings': 0.05,
    'Entertainment': 0.05,
    'Clothing': 0.03,
    'Miscellaneous': 0.02
}

income_data = pd.DataFrame({
    'Source': ['Salary', 'Investments', 'Freelance work'],
    'Amount': [5000, 1000, 2000]
})

expenses_data = pd.DataFrame({
    'Category': ['Housing', 'Transportation', 'Food', 'Utilities', 'Insurance', 'Medical', 'Savings', 'Entertainment', 'Clothing', 'Miscellaneous'],
    'Amount': [1500, 750, 500, 500, 250, 250, 250, 250, 150, 100]
})

# Define functions
def generate_spending_chart():
    chart_data = {key: val * monthly_income for key, val in spending_categories.items()}
    chart_df = pd.DataFrame.from_dict(chart_data, orient="index", columns=["Amount"])
    chart_df.reset_index(inplace=True)
    chart_df.rename(columns={'index': 'Category'}, inplace=True)

    chart = alt.Chart(chart_df).mark_bar().encode(
        x='Amount:Q',
        y=alt.Y('Category:N', sort=list(spending_categories.keys())),
        color=alt.Color('Category:N', legend=None)
    ).properties(
        width=700,
        height=400,
        title='Monthly Spending'
    )

    return chart

def generate_income_chart():
    chart = alt.Chart(income_data).mark_bar().encode(
        x='Amount:Q',
        y='Source:N',
        color=alt.Color('Source:N', legend=None)
    ).properties(
        width=700,
        height=400,
        title='Monthly Income'
    )

    return chart

def generate_expenses_chart():
    chart = alt.Chart(expenses_data).mark_bar().encode(
        x='Amount:Q',
        y='Category:N',
        color=alt.Color('Category:N', legend=None)
    ).properties(
        width=700,
        height=400,
        title='Monthly Expenses'
    )

    return chart

# Define the app
def app():
    st.title("Personal Finance Management")

    monthly_income = st.number_input("What is your monthly income?", value=5000)

    st.subheader("Monthly Breakdown")

    st.altair_chart(generate_spending_chart(), use_container_width=True)
    st.altair_chart(generate_income_chart(), use_container_width=True)
    st.altair_chart(generate_expenses_chart(), use_container_width=True)

    st.subheader("Analysis")

    expenses_total = expenses_data['Amount'].sum()
    savings_total = monthly_income - expenses_total

    st.write("Total Expenses: $", expenses_total)
    st.write("Total Savings: $", savings_total)

    st.subheader("Tips")

    st.write("- Review your monthly spending and identify areas where you can cut back.")
    st.write("- Consider setting up automatic savings transfers to help you reach your financial goals.")
    st.write("- Check your credit score regularly and work to improve it if necessary.")
