# -------------------------------------
# Importing libraries
# -------------------------------------
import pandas as pd
import folium 
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

# ----------------------------
# Configuration
# ----------------------------

st.set_page_config(page_icon=":fork_and_knife:",
                   page_title='Overhall', 
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

# -------------------------------------
# Functions
# -------------------------------------

def create_map(dataframe):
    f = folium.Figure(width=1920, height=1080)

    m = folium.Map(max_bounds=True).add_to(f)

    marker_cluster = MarkerCluster().add_to(m)

    for _, line in dataframe.iterrows():

        name = line["restaurant_name"]
        price_for_two = round(line["price_dollar"], 2)
        cuisine = line["cuisines"]
        rating = line["aggregate_rating"]
        color = f'{line["color_name"]}'

        html = "<p><strong>{}</strong></p>"
        html += "<p>Price for two: ${}"
        html += "<br />Type: {}"
        html += "<br />Aggregate Rating: {}/5.0"
        html = html.format(name, price_for_two, cuisine, rating)

        popup = folium.Popup(
            folium.Html(html, script=True),
            max_width=500,
        )

        folium.Marker(
            [line["latitude"], line["longitude"]],
            popup=popup,
            icon=folium.Icon(color=color, icon="home", prefix="fa"),
        ).add_to(marker_cluster)

    folium_static(m, width=1024, height=768)


# ================================================================================================
#                             Beginning of the code's logical structure
# ================================================================================================

# ----------------------------
# Importing dataset
# ----------------------------
# import file
data_source = pd.read_csv('zomato_clean.csv')

# create a copy of the dataframe 
df=data_source.copy()


# ----------------------------
# Creating side bar
# ----------------------------
                              
image = Image.open('great_food_logo.png')
st.sidebar.image(image, width=140)

country = st.sidebar.multiselect(
    "Select the Country:",
    options=df['country_name'].unique().tolist(),
    default=df['country_name'].unique().tolist(),
)

# enable the filter for countries
selected_rows =  df['country_name'].isin(country)
df = df.loc[selected_rows , :]

st.sidebar.markdown( '''---''' )
st.sidebar.markdown ('###### Powered by Isabela Barbosa')
st.sidebar.markdown ('###### Data Scientist @ Comunidade DS')

#==================================================
# Layout Overall page
#==================================================

st.title( ':fork_and_knife:Great Food')
st.markdown( '### The place to find your new favorite restaurant!' )
st.markdown( '''---''' )
    

with st.container():
    st.markdown( "## Our Numbers :chart_with_upwards_trend:")

    col1, col2, col3, col4, col5 = st.columns( 5, gap='large')
    with col1:
        number_of_countries = df['country_name'].nunique()
        col1.metric( 'Registread Countries ',  number_of_countries )       

    with col2:
        number_of_cities = df['city'].nunique()
        col2.metric( 'Registread Cities ',  number_of_cities)

    with col3:
        registred_restaurants = (f"{df['restaurant_id'].nunique():,}".replace(',', ','))
        col3.metric( 'Registred Restaurants', registred_restaurants )

    with col4:
        number_of_cuisines = df['cuisines'].nunique()
        col4.metric( 'Types of Cuisines', number_of_cuisines )
         
    with col5:
        sum_votes = df['votes'].sum()
        votes = (f"{sum_votes:,}".replace(',', ','))
        col5.metric('Reviews Received', value=votes)
        

st.markdown( '''---''' )
with st.container():
    st.markdown( "## Check the map bellow to find Great Food locations 🗺️" )
    create_map(df)
    