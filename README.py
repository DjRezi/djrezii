
# Import libraries
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib
import streamlit as st
from preprocessing import preprocess_data

# Load dataset
df = pd.read_csv('diet_data.csv')

# Preprocess data
df_preprocessed = preprocess_data(df)

# Sidebar for registration
registration_status = st.sidebar.checkbox("Register as a new user")
if registration_status:
    # Function for registering new user
    def register_user():
        st.write("Please fill in the following information to register:")
        name = st.text_input("Name:")
        age = st.number_input("Age:", min_value=0, max_value=150)
        gender = st.selectbox("Gender:", ['Male', 'Female'])
        height = st.number_input("Height (cm):", min_value=0, max_value=250)
        weight = st.number_input("Weight (kg):", min_value=0, max_value=500)
        activity_level = st.selectbox("Activity level:", ['Sedentary', 'Lightly Active',
                                                            'Moderately Active', 'Very Active'])
        calories_per_day = st.number_input("Daily calories intake (kcal):", min_value=0, max_value=10000)
        new_user_data = pd.DataFrame({
            "name": [name],
            "age": [age],
            "gender": [gender],
            "height": [height],
            "weight": [weight],
            "activity_level": [activity_level],
            "calories_per_day": [calories_per_day]
        })
        return new_user_data
        
    # Get new user data and write to CSV file
    new_user_data = register_user()
    df_new_user = pd.concat([df_preprocessed, new_user_data])
    try:
        df_new_user.to_csv("diet_data.csv", index=False)
    except:
        st.error('Error: Could not register user.')

    # Update preprocessed data with new user data
    df_preprocessed = df_new_user

# Split into training and testing sets
X = df_preprocessed.drop('BMI', axis=1)
y = df_preprocessed['BMI']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train decision tree model using cross-validation
dt_model = DecisionTreeClassifier(max_depth=3, random_state=42)
cv_scores = cross_val_score(dt_model, X_train, y_train, cv=5)
accuracy = cv_scores.mean()

# Display model accuracy
st.markdown(f"Model accuracy: {accuracy:.2f}")

# Save model
joblib.dump(dt_model, 'diet_planner_model.pkl')

