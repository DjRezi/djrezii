import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# Get the absolute path of the directory containing this script
dir_path = os.path.dirname(os.path.abspath(__file__))

# Load the machine learning model
model_path = os.path.join(dir_path, 'model.pkl')
if os.path.exists(model_path):
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
else:
    # Display error message if model file is not found
    st.error("Model file not found. Please check that 'model.pkl' exists in the same directory as this script.")
    st.stop()

# Load sample data for demo purposes
data = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv")

# Create a form for the user to input their information
st.title('Diet Recommendation App')
st.header('Enter Your Information')
height = st.slider('Height (in cm)', 100, 250, 150)
weight = st.slider('Weight (in kg)', 30, 300, 70)
age = st.slider('Age', 1, 120, 30)
gender = st.radio('Gender', ('Male', 'Female'))
blood_type = st.radio('Blood Type', ('A', 'B', 'AB', 'O'))
country = st.text_input('Country')

# Make a prediction using the machine learning model
input_data = pd.DataFrame({
    'Height': [height],
    'Weight': [weight],
    'Age': [age],
    'Gender': [gender],
    'Blood Type': [blood_type],
    'Country': [country]
})

if 'Outcome' in data.columns:
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']
else:
    X = data.drop('Class', axis=1)
    y = data['Class']
    
model.fit(X, y)
prediction = model.predict(input_data)

# Display the recommended diet to the user
st.header('Recommended Diet')
st.write(prediction)

# Add a chart to track progress over time
st.header('Progress Chart')
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Week', 'Weight', 'BMI'])
st.line_chart(chart_data)
