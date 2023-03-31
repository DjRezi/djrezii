import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import requests

# Define layout
st.title("Calorie Tracker")

# Define form fields
with st.form(key='my_form'):
    food_name = st.text_input(label='Enter food name')
    calories = st.number_input(label='Enter calories')
    date = st.date_input(label='Enter date')
    submit_button = st.form_submit_button(label='Submit')

# Load data
data = pd.DataFrame({
    'food_name': ['chicken', 'pasta', 'salad'],
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
st.write("Total Calories Consumed Last Week:", total_calories)

# Calculate recommended daily caloric intake
gender = st.radio(label="Select your gender", options=["Male", "Female"])
age = st.number_input(label="Enter your age")
height = st.number_input(label="Enter your height in cm")
weight = st.number_input(label="Enter your weight in kg")
activity_level = st.selectbox(label="Select your activity level", options=["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extremely Active"])
goal = st.radio(label="Select your goal", options=["Lose weight", "Maintain weight", "Gain weight"])

if submit_button:
    # Add new data to dataset
    new_data = pd.DataFrame({'food_name': [food_name], 'calories': [calories], 'date': [date]})
    data = pd.concat([data, new_data], ignore_index=True)

    # Calculate total calories for last week
    last_week = datetime.now() - timedelta(days=7)
    week_data = data[data['date'] > last_week]
    total_calories = week_data['calories'].sum()

    # Display total calories for last week
    st.write("Total Calories Consumed Last Week:", total_calories)

    # Calculate recommended daily caloric intake
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
    elif goal == "Gain weight":
        daily_calories = tdee + 500
    else:
        daily_calories = tdee

