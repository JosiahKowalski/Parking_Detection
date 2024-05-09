import base64
import os

import PIL
import streamlit as st
import openai
import textwrap
from IPython.display import display, Image
from Parking_Lot import Parking_Lot
import google.generativeai as genai

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
genai.configure(api_key=st.secrets['PALM_API_KEY'])


# for openai?
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_number_of_empty_spots(parking_lot) -> (int, str):
    response = predict_number_of_cars(parking_lot)
    return parking_lot.parking_spots - int(response), response


def predict_number_of_cars(parking_lot):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(
        ["How many cars are in this image, answer only with a number with no punctuation?",
         parking_lot.get_pil_image()], stream=True)
    response.resolve()
    return response.text


st.title('Parking Detection')
# 15 cars
parking_lot1 = Parking_Lot('Parking Lot 1', 'parking_image_1.jpg', 144)
# 84 cars I think
parking_lot2 = Parking_Lot('Parking Lot 2', 'parking_image_2.jpg', 360)  # guessed

with st.sidebar:
    lot = st.radio('Select an image',
                   [parking_lot1, parking_lot2])

if st.button('Predict'):
    spots, cars = get_number_of_empty_spots(lot)
    st.image(lot.image_path, caption=lot.name, use_column_width=True)
    st.write(f'Number of empty spots: {spots}  \nNumber of cars: {cars}')
