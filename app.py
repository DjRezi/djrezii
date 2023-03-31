import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

# Define layout
st.set_page_config(page_title="Calorie Tracker", page_icon=":hamburger:", layout="wide")
st.title("Calorie Tracker")

# Define form fields
with st.form(key='my_form'):
    food_name = st.text_input(label='Enter food name')
    calories = st.number_input(label='Enter calories', min_value=1)
    date = st.date_input(label='Enter date', value=datetime.now())
    submit_button = st.form_submit_button(label='Add')

# Load data
data = pd.DataFrame({
    'food_name': ['Chicken', 'Pasta', 'Salad'],
    'calories': [450, 600, 200],
    'date': ['2022-03-29', '2022-03-30', '2022-03-31']
})

# Convert date column to datetime
data['date'] = pd.to_datetime(data['date'])

# Filter data by date
last_week = datetime.now() - timedelta(days=7)
week_data = data[data['date'] > last_week]

# Calculate total calories for last week
total_calories = week_data['calories'].sum()

# Display total calories for last week
st.write(f"Total Calories Consumed Last Week: {total_calories}")

# Calculate recommended daily caloric intake
st.write("")
st.write("Recommended Daily Caloric Intake")
gender = st.radio(label="Select your gender", options=["Male", "Female"], index=0)
age = st.number_input(label="Enter your age", min_value=1, max_value=120, value=18)
height = st.number_input(label="Enter your height in cm", min_value=50, max_value=300, value=170)
weight = st.number_input(label="Enter your weight in kg", min_value=1, max_value=500, value=70)
activity_level = st.selectbox(label="Select your activity level", options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"], index=2)
goal = st.radio(label="Select your goal", options=["Lose weight", "Maintain weight", "Gain weight"], index=1)

if submit_button:
    # Add new data to dataset
    new_data = pd.DataFrame({'food_name': [food_name.capitalize()], 'calories': [calories], 'date': [date]})
    data = pd.concat([data, new_data], ignore_index=True)

    # Calculate total calories for last week
    last_week = datetime.now() - timedelta(days=7)
    week_data = data[data['date'] > last_week]
    total_calories = week_data['calories'].sum()

    # Display total calories for last week
    st.write(f"Total Calories Consumed Last Week: {total_calories}")

    # Calculate recommended daily caloric intake
    if gender == "Male":
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

    if activity_level == "Sedentary":
        tdee = bmr * 1.2
    elif activity_level == "Lightly Active":
        tdee = bmr * 1.375
    elif activity_level
