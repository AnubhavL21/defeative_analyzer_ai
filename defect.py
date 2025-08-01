import os
import streamlit as st
from dotenv import load_dotenv  
load_dotenv() 

import google.generativeai as genai

from PIL import Image # pillow is used to load ,save and manipulate the image

st.set_page_config(page_title="Defeat Detection", page_icon='🤖' , layout="wide")

st.title('AI Assistant for :green[Structural Defeat and Analysis]')
st.subheader(':blue[Prototype for automated strurctural defeat analysis]',divider=True)

with st.expander('About the application'):
    st.markdown('''This prototype is used to detect the structural defects and analyze the defects using AI- powered system.
                - **DEfeact Detection** : Automatically detects the structural defects in the image.
                - **Recommendations** : Provides solution and recommnetations based on the detected defects.
                - **Report Generation** : Create a detailed report of the analysis.''')
    
key=os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=key)

st.subheader('Upload an image for analysis')
input_image=st.file_uploader('Upload an image', type=['jpg', 'jpeg', 'png'])
if input_image:
    img=Image.open(input_image)
    st.image(img,caption='uploaded_image')
    
prompt= f''' Act as a Civil Engineer and provide the poper explaination for below given questions
    1.Does the image contain any cracks or defects?
    2.What type of defective the image contains? catgorize it into two type [fixable,unfixable]
    3.if the image contains fixable defects, provide the solution for it.
    4.if the image contains unfixeable defects then provide the solution accoreding to it.
    5.Estimate the cost for the fixale defects.
    6.Analyse the image and recommend the possible cause for it.
    and aslo provide the possible solution to prevent it in future
    7.provide the percentage of the defeact whether it is dangorous or not on scale of 1 to 100'''
    
model=genai.GenerativeModel('gemini-2.0-flash')

def generate_result(prompt,img):
    result=model.generate_content(f''' Using the given prompt {prompt} analyze the giben image{img} and 
                                  genarate the result based on the prompt''',)
    return result.text
submit=st.button('Analyze the defect')

if submit:
    with st.spinner('Analyzing the image...'):
        response=generate_result(prompt,img)
        
        st.markdown(':green[Result]')
        st.write(response)