import os
import pickle
import streamlit as st
import pandas as pd

# Load model
dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(dir_path, 'model.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Load sample dataset
df = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv')

# Sidebar - User Input Features
st.sidebar.title('User Input Features')
# Collects user input features into dataframe
def user_input_features():
    age = st.sidebar.slider('Age', 1, 100, 25)
    gender = st.sidebar.selectbox('Gender',('Male','Female'))
    height = st.sidebar.slider('Height in cm', 100, 250, 175)
    weight = st.sidebar.slider('Weight in kg', 20, 200, 70)
    country = st.sidebar.selectbox('Country', ('USA', 'Canada', 'UK', 'Australia'))
    blood_type = st.sidebar.selectbox('Blood Type', ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'))
    data = {'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'country': country,
            'blood_type': blood_type}
    features = pd.DataFrame(data, index=[0])
    return features

df_new = user_input_features()

# Main Panel
st.header('Recommended Diet for Weight Management')

# Show the user input features
st.write('User Input features:')
st.write(df_new)

# Make recommendations
prediction = model.predict(df_new)
if prediction == 1:
    st.write('We recommend a diet plan for weight gain.')
else:
    st.write('We recommend a diet plan for weight loss.')

# Show sample dataset
st.subheader('Sample Dataset')
st.write(df.head())
