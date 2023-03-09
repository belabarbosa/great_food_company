# -------------------------------------
# Importing libraries
# -------------------------------------
import streamlit as st
from PIL import Image


st.set_page_config(page_icon="📌",
                   page_title='Home',
                   layout='wide'
)
  

# Hiding Streamilit style
hide_st_style= """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# ----------------------------
# Creating side bar
# ----------------------------

image = Image.open('great_food_logo.png')
st.sidebar.image(image, width=140)
st.sidebar.markdown( '### The place to find your new favorite restaurant!' )
st.sidebar.markdown( '''---''' )
st.sidebar.markdown ('###### Powered by Isabela Barbosa')
st.sidebar.markdown ('###### Data Scientist @ Comunidade DS')


#==================================================
# Layout Home Page
#==================================================

st.write( "# :bar_chart:Great Food Growth Dashboard" ) 
st.markdown( '''---''' )
st.markdown(
    """    
    ### What you are going to find on this dashboard:
    - **Overhall:**
        - Company's numbers.
        - Locations.
    
    - **Countries:**
        - Restaurants by Countries.
        - Cities by Contries.
        - Average Number of Reviews.
        - Average Price of a Meal for Two.
        - Number of Different Cuisines Available.
    
    - **Cities:**
        - Top 10 Cities With Restaurants Rated Above 4.
        - Top 10 Cities With Restaurants Rated Below 2.5.
        - Top 10 Cities With the Most Different Types of Cuisine.
    
    - **Cuisines:**
        - Best Restaurant of the Main Cuisines Types.
        - Types of Cuisines.
        - Top 10 Restaurants.
        
    ### Dashboard support:
        For questions, suggestions or any other subject related to this dashboard, feel free to contact me on LinkedIn.
    """ )
    