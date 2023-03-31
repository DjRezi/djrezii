import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

# Define layout
st.set_page_config(page_title="Calorie Tracker", page_icon=":fork_and_knife:")
st.title("Calorie Tracker")

# Define form fields
with st.form(key='my_form'):
    food_name = st.text_input(label='Enter food name')
    calories = st.number_input(label='Enter calories', min_value=1)
    date = st.date_input(label='Enter date', value=datetime.today())
    submit_button = st.form_submit_button(label='Add to tracker')

# Load data from CSV or create a new DataFrame
if 'calories.csv' not in st.session_state:
    st.session_state['calories.csv'] = pd.DataFrame(columns=['food_name', 'calories', 'date'])
data = st.session_state['calories.csv']

# Add new entry to the DataFrame if form is submitted
if submit_button:
    new_entry = pd.DataFrame({'food_name': [food_name], 'calories': [calories], 'date': [date]})
    data = pd.concat([data, new_entry], ignore_index=True)
    st.session_state['calories.csv'] = data

# Filter data by date range
start_date = st.date_input('Start date', value=(datetime.today() - timedelta(days=6)))
end_date = st.date_input('End date', value=datetime.today())
filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]

# Calculate total calories for date range
total_calories = filtered_data['calories'].sum()

# Display total calories for date range
st.subheader(f"Total Calories Consumed from {start_date} to {end_date}:")
st.write(total_calories)

# Calculate recommended daily caloric intake
st.header("Calculate Recommended Daily Caloric Intake")

gender = st.selectbox("Select your gender", options=["Male", "Female"])
age = st.slider("Enter your age", min_value=0, max_value=120, value=25, step=1)
height = st.slider("Enter your height in cm", min_value=100, max_value=250, value=175, step=1)
weight = st.slider("Enter your weight in kg", min_value=30, max_value=300, value=70, step=1)
activity_level = st.selectbox("Select your activity level", options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
goal = st.selectbox("Select your goal", options=["Lose weight", "Maintain weight", "Gain weight"])

if gender == "Male":
    bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
else:
    bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

if activity_level == "Sedentary":
    tdee = bmr * 1.2
elif activity_level == "Lightly Active":
    tdee = bmr * 1.375
elif activity_level == "Moderately Active":
    tdee = bmr * 1.55
elif activity_level == "Very Active":
    tdee = bmr * 1.725
else:
    tdee = bmr * 1.9

if goal == "Lose weight":
    daily_calories = tdee - 500
elif goal
