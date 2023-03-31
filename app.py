import streamlit as st

# Define the Streamlit app title
st.title("Personal Finance Management App")

# Define the sidebar with user inputs
st.sidebar.title("User Inputs")

# Define user input fields and retrieve values
income = st.sidebar.number_input("Enter your monthly income:", min_value=0)
expenses = st.sidebar.number_input("Enter your monthly expenses:", min_value=0)
savings_goal = st.sidebar.number_input("Enter your savings goal:", min_value=0)

# Calculate remaining income and display to user
remaining_income = income - expenses
st.write(f"Your remaining income is ${remaining_income} per month.")

# Calculate how long it will take to reach savings goal and display to user
if remaining_income > 0:
    months_to_goal = round(savings_goal / remaining_income)
    st.write(f"At your current rate of saving, it will take you {months_to_goal} months to reach your savings goal.")
else:
    st.write("You are not currently saving enough to reach your savings goal.")

# Create a chart to display income and expenses
chart_data = {"Income": income, "Expenses": expenses}
chart_df = pd.DataFrame.from_dict(chart_data, orient="index", columns=["Amount"])
st.write("## Income vs. Expenses")
st.bar_chart(chart_df)

# Create a line chart to track savings progress
savings_data = {"Savings Goal": savings_goal, "Savings Progress": 0}
savings_df = pd.DataFrame.from_dict(savings_data, orient="index", columns=["Amount"])
st.write("## Savings Progress")
savings_chart = st.line_chart(savings_df)

# Define a button to update savings progress
if remaining_income > 0:
    update_button = st.button("Update Savings Progress")
    if update_button:
        # Calculate updated savings progress and update chart
        savings_progress = savings_goal - remaining_income
        savings_data["Savings Progress"] = savings_progress
        savings_df = pd.DataFrame.from_dict(savings_data, orient="index", columns=["Amount"])
        savings_chart = st.line_chart(savings_df)
        st.success("Savings progress updated successfully!")
    else:
        st.write("Click the button to update your savings progress.")
else:
    st.write("You are not currently saving enough to update your savings progress.")
