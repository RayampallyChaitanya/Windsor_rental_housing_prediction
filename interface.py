# Importing the required libraries
import streamlit as st
import pandas as pd 
import numpy as np 
import pickle 
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from PIL import Image
import seaborn as sns
import base64


# loading in the model to predict on the data 
pickle_in = open('grid_search_rf.pkl', 'rb') 
classifier = pickle.load(pickle_in) 

# Defining the function which will make the prediction using 
# the data which the user inputs 
def prediction(houseType, bedrooms, bathrooms, parking, petfriendly, laundry, personaloutdoorspace, region, size): 

    prediction = classifier.predict( 
        [[houseType, bedrooms, bathrooms, parking, petfriendly, laundry, personaloutdoorspace, region, size]]) 
    print(prediction) 
    return prediction 

# Defining the function which displays the content as markdown header
def result_function():
    
    result_header = """
    <div style = "background-color:#8FBC8F;padding:13px">
    <h3 style ="color:black;text-align:center;">Windsor House Rental Prediction Results </h3>
    </div>
    """
    st.markdown(result_header, unsafe_allow_html = True)
    
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# this is the main function in which we define our webpage 
def main():
    
    
    # giving the webpage a title 
    #st.title("Python Project") 

    # here we define some of the front end elements of the web page like 
    # the font and background color, the padding and the text to be displayed 
    html_temp = """ 
    <div style ="background-color:#8ebf42;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Windsor House Rental Prediction </h1> 
    </div> 
    """
       
    # this line allows us to display the front end aspects we have 
    # defined in the above code 
    st.markdown(html_temp, unsafe_allow_html = True)
    
    set_png_as_page_bg('windsor-canada.jpg')


 
    # Organizing the elements of the web page in a interactive way by defining them in the web page columns
    # Defining a dictionary to get the user input value for each interactive element
    col1,col2,col3 = st.beta_columns(3)
    
    houseType_dict = { 0:"Apartment",
                     1:"Basement", 2:"Condo", 3:"Duplex/Triplex", 4:"House", 5:"Townhouse"} 
    houseType = col1.selectbox( 
                    'House Type',options=list(houseType_dict.items()),format_func = lambda x:x[1])
    
    bedrooms_dict = {0:'1', 1:'1+Den', 2:'2',3:'2+Den',4:'3',5:'3+Den',6:'4',7:'4+Den',8:'5+',9:'Bachelor/Studio'}
    bedrooms = col2.selectbox(
        'Number of Bedrooms',options=list(bedrooms_dict.items()),format_func = lambda x:x[1])
    
    
    
    bathrooms_dict = {1:'1', 1.5:'1.5', 2:'2', 2.5:'2.5', 3:'3'}
    bathrooms = col3.selectbox("Number of Bathrooms", options=list(bathrooms_dict.items()),format_func = lambda x:x[1])
    
    parking_dict = {0:'0', 1:'1', 2:'2', 3:'3'}
    parking = col1.selectbox("Number of Parking",  options=list(parking_dict.items()),format_func = lambda x:x[1])
    
    pet_friendly_dict = {0:'Limited',1:'No',2:'Yes'}
    petfriendly = col1.selectbox('Pet-Friendly',options=list(pet_friendly_dict.items()),format_func = lambda x:x[1])
    
    
    laundry_dict = {0:'In Building',1:'In Building/In Unit', 2:'In Unit',3:'Not Included'}
    laundry = col3.selectbox('Laundry',options=list(laundry_dict.items()),format_func = lambda x:x[1])
    
    personal_outdoor_space_dict = {0:'Balcony', 1:'Not Applicable', 2:'Yard'}
    personaloutdoorspace = col2.selectbox('Personal Outdoor Space',
                                        options=list(personal_outdoor_space_dict.items()),format_func=lambda x:x[1])
    
    size_dict = {0:'Less Than 500',
                1:'In Between 500-999',
                2:'In Between 1000-1499',
                3:'In Between 1500-1999',
                4:'In Between 2000-2499',
                5:'Greater Than 2500'}
    size = col2.selectbox("Size - Sq.Ft.", options=list(size_dict.items()),format_func=lambda x:x[1])
    
    
    region_dict = {0:'City Centre NW Walkerville ',
                  1:'East East Walkerville',
                  2:'East Forest Glade',
                  3:'East Riverside',
                  4:'Riverside',
                   5:'Roseland',
                   6:'Sandwich Ojibway West Malden',
                   7:'South Central West Walkerville Remington P',
                   8:'South East Malden',
                   9:'South Walkerville West Fontainbleu Walker',
                   10:'University South Cameron',
                   11:'West Forest Glade East Fontainbleu'
                  }
    region = col3.selectbox('Windsor Region',options=list(region_dict.items()),format_func=lambda x:x[1])
    
  
    result ="" 
    

    # the below line ensures that when the button called 'Predict' is clicked, 
    # the prediction function defined above is called to make the prediction 
    # and store it in the variable result 
    if st.button("Predict Rent"):
        
        result = prediction(houseType[0], bedrooms[0], bathrooms[0], parking[0], petfriendly[0],
                            laundry[0],personaloutdoorspace[0], region[0], size[0])
        result_function()
        # According to the predicted result, displaying the price as markdown header
        if result == 0:
            result_header_1 = """
            <div style = "background-color:#D8D8D8;padding:8px">
            <h4 style ="color:black;text-align:center;">The Rent is Below $500 </h4>
            </div>
            """
            st.markdown(result_header_1, unsafe_allow_html = True)
        if result == 1:
            result_header_2 = """
            <div style = "background-color:#D8D8D8;padding:8px">
            <h4 style ="color:black;text-align:center;">The Rent is Between $500 - $1000 </h4>
            </div>
            """
            st.markdown(result_header_2, unsafe_allow_html = True)
        if result == 2:
            result_header_3 = """
            <div style = "background-color:#D8D8D8;padding:8px">
            <h4 style ="color:black;text-align:center;">The Rent is Between $1000 - $1500 </h4>
            </div>
            """
            st.markdown(result_header_3, unsafe_allow_html = True)
        if result == 3:
            result_header_4 = """
            <div style = "background-color:#D8D8D8;padding:8px">
            <h4 style ="color:black;text-align:center;">The Rent is Between $1500 - $2000 </h4>
            </div>
            """
            st.markdown(result_header_4, unsafe_allow_html = True)
        if result == 4:
            result_header_5 = """
            <div style = "background-color:#D8D8D8;padding:8px">
            <h4 style ="color:black;text-align:center;">The Rent is Between $2000 - $2500 </h4>
            </div>
            """
            st.markdown(result_header_5, unsafe_allow_html = True)
        if result == 5:
            result_header_6 = """
            <div style = "background-color:#D8D8D8;padding:8px">
            <h4 style ="color:black;text-align:center;">The Rent is Above $2500 </h4>
            </div>
            """
            st.markdown(result_header_6, unsafe_allow_html = True)           
         
    
        

if __name__=='__main__': 
    main() 
