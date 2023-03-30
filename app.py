import requests
import json
import pandas as pd
import streamlit as st
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# download data from USDA's FoodData Central API
url = 'https://api.nal.usda.gov/fdc/v1/foods/list?pageSize=1000&api_key=a1pqdXRMEE1FHtnOa5TlsPwcM3Op2ybvdDmWbYoo'
response = requests.get(url)
data = json.loads(response.text)

# create dataframe with nutrient values
foods = []
for item in data['foods']:
    nutrients = {}
    for nutrient in item['foodNutrients']:
        nutrients[nutrient['nutrientName']] = nutrient['value']
    nutrients['foodName'] = item['description']
    foods.append(nutrients)
df = pd.DataFrame(foods)

# split data into training and testing sets
X = df.drop(['foodName', 'Energy'], axis=1)
y = df['Energy']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# train decision tree model
model = DecisionTreeRegressor()
model.fit(X_train, y_train)

# create function to generate weight loss plan
def generate_weight_loss_plan(weight, height, age, blood_type, gender, country):
    # lookup nutrient values for user's country and blood type
    nutrients = df[(df['Country'] == country) & (df['Blood Type'] == blood_type)].mean()
    nutrients = nutrients.drop(['Country', 'Blood Type', 'Energy'])

    # create dataframe with user information
    user = pd.DataFrame({
        'Weight': [weight],
        'Height': [height],
        'Age': [age],
        'Gender': [gender],
    })

    # add user information to dataframe with nutrient values
    for col in user.columns:
        nutrients[col] = user[col].values[0]

    # predict daily calorie intake
    daily_calories = model.predict(nutrients.values.reshape(1, -1))[0]
    weight_loss_calories = daily_calories - 500  # aim for 1 pound weight loss per week
    return f'Your recommended daily calorie intake for weight loss is {weight_loss_calories} calories.'

# create web app with Streamlit
st.title('Weight Loss Diet Generator')

weight = st.number_input('Enter your weight (in kg):')
height = st.number_input('Enter your height (in cm):')
age = st.number_input('Enter your age:')
blood_type = st.selectbox('Select your blood type:', ['A', 'B', 'AB', 'O'])
gender = st.radio('Select your gender:', ['Male', 'Female'])
country = st.selectbox('Select your country:', ['United States', 'Canada', 'United Kingdom'])

if st.button('Generate Diet Plan'):
    diet_plan = generate_weight_loss_plan(weight, height, age, blood_type, gender, country)
    st.write(diet_plan)
