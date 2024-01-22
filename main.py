import streamlit as st
import pickle
import json
import numpy as np

# Load the model and columns
model_file = 'bghouse.pickle'
columns_file = 'columns.json'

with open(model_file, 'rb') as f:
    model = pickle.load(f)

with open(columns_file, 'r') as f:
    columns = json.load(f)['data_columns']

# Exclude 'total_sqft', 'bhk', 'bath' from the location dropdown
locations = [col for col in columns if col not in ['total_sqft', 'bhk', 'bath']]

def predict_price(location, total_sqft, bhk, bath):
    loc_index = columns.index(location.lower())

    x = np.zeros(len(columns))
    x[0] = total_sqft
    x[1] = bhk
    x[2] = bath
    if loc_index >= 0:
        x[loc_index] = 1

    return model.predict([x])[0]
def main():
    # Set a background image
    st.markdown(
        """
        <style>
        body {
            background-image: url('property-2.jpg');
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    st.title('Bengaluru Housing Price Prediction App')

    # Location selection excluding 'total_sqft', 'bhk', 'bath'
    location = st.selectbox('Select Location', locations)

    # Features input section
    st.header('Enter Property Details:')
    total_sqft = st.number_input('Total Square Feet Area', min_value=1)
    bhk = st.number_input('Number of Bedrooms (BHK)', min_value=1)
    bath = st.number_input('Number of Bathrooms', min_value=1)

    # Prediction button
    if st.button('Predict Price'):
        result = predict_price(location, total_sqft, bhk, bath)
        st.success(f'Predicted Price: {result:.2f} Lakhs Indian Rupees')

if __name__ == '__main__':
    main()
