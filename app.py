import streamlit as st
import requests
from datetime import datetime

'''
# TaxiFareModel front
'''

st.markdown('''
Remember that there are several ways to output content into your web page...

Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
''')

'''
## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

1. Let's ask for:
- date and time
- pickup longitude
- pickup latitude
- dropoff longitude
- dropoff latitude
- passenger count
'''
with st.form(key='params_for_api'):

    # Date and Time
    pickup_date = st.date_input('Pickup date', datetime.now())
    pickup_time = st.time_input('Pickup time', datetime.now().time())

    # Location inputs
    col1, col2 = st.columns(2)
    with col1:
        pickup_longitude = st.number_input('Pickup longitude', value=-73.950655)
        dropoff_longitude = st.number_input('Dropoff longitude', value=-73.984365)
    with col2:
        pickup_latitude = st.number_input('Pickup latitude', value=40.783282)
        dropoff_latitude = st.number_input('Dropoff latitude', value=40.769802)

    passenger_count = st.number_input('Passenger count', min_value=1, max_value=8, value=1)

    submitted = st.form_submit_button('Get Fare Prediction')

if submitted:
    # Combine date and time
    pickup_datetime = f"{pickup_date} {pickup_time}"

    '''
    ## Once we have these, let's call our API in order to retrieve a prediction

    See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

    🤔 How could we call our API ? Off course... The `requests` package 💡
    '''

    url = 'https://taxifare.lewagon.ai/predict'

    if url == 'https://taxifare.lewagon.ai/predict':

        st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

    '''

    2. Let's build a dictionary containing the parameters for our API...'''
    params = {
            "pickup_datetime": pickup_datetime,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "passenger_count": passenger_count
        }

    '3. Lets call our API using the `requests` package...'
    response = requests.get(url, params=params)

    '''4. Let's retrieve the prediction from the **JSON** returned by the API...'''

    ## Finally, we can display the prediction to the user

    if response.status_code == 200:
        prediction = response.json().get('prediction', response.json().get('fare'))
        st.success(f"Estimated fare: ${prediction:.2f}")

        # Show a simple map of the pickup and dropoff locations
        st.map({
            'lat': [pickup_latitude, dropoff_latitude],
            'lon': [pickup_longitude, dropoff_longitude]
        })
    else:
        st.error("Error making prediction. Please try again.")
        st.write(f"API Response: {response.status_code} - {response.text}")
