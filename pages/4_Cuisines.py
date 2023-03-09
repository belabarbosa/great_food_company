# -------------------------------------
# Importing libraries
# -------------------------------------
import pandas as pd
import re
import plotly.express as px
import folium 
import seaborn as se
import plotly.graph_objects as go
import numpy as np
from haversine import haversine
import inflection
from PIL import Image
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS


# -------------------------------------
# Functions
# -------------------------------------

def top_cuisines( df ):

    cuisines = {
        "Italian": "",
        "American": "",
        "Arabian": "",
        "Japanese": "",
        "Brazilian": "",
    }

    cols = [
        "restaurant_id",
        "restaurant_name",
        "country_name",
        "city",
        "cuisines",
        "price_dollar",
        "aggregate_rating",
        "votes",
    ]

    for key in cuisines.keys():

        lines = df["cuisines"] == key

        cuisines[key] = (
            df.loc[lines, cols]
            .sort_values(["aggregate_rating", "restaurant_id"], ascending=[False, True])
            .iloc[0, :]
            .to_dict()
        )

    return cuisines


def write_metrics( df ):

    cuisines = top_cuisines( df )

    italian, american, arabian, japonese, brazilian = st.columns(len(cuisines))

    with italian:
        st.metric(
            label=f'Italian: {cuisines["Italian"]["restaurant_name"]}',
            value=f'{cuisines["Italian"]["aggregate_rating"]}/5.0',
            help=f"""
            Country: {cuisines["Italian"]['country_name']}\n
            City: {cuisines["Italian"]['city']}\n
            Average price of meal for two (U.S. Dollar): {cuisines["Italian"]['price_dollar']}
            """,
        )

    with american:
        st.metric(
            label=f'American: {cuisines["American"]["restaurant_name"]}',
            value=f'{cuisines["American"]["aggregate_rating"]}/5.0',
            help=f"""
            Country: {cuisines["American"]['country_name']}\n
            City: {cuisines["American"]['city']}\n
            Average price of meal for two (U.S. Dollar) {cuisines["American"]['price_dollar']}
            """,
        )

    with arabian:
        st.metric(
            label=f'Arabian: {cuisines["Arabian"]["restaurant_name"]}',
            value=f'{cuisines["Arabian"]["aggregate_rating"]}/5.0',
            help=f"""
            Country: {cuisines["Arabian"]['country_name']}\n
            City: {cuisines["Arabian"]['city']}\n
            Average price of meal for two (U.S. Dollar): {cuisines["Arabian"]['price_dollar']}
            """,
        )

    with japonese:
        st.metric(
            label=f'Japanese: {cuisines["Japanese"]["restaurant_name"]}',
            value=f'{cuisines["Japanese"]["aggregate_rating"]}/5.0',
            help=f"""
            Country: {cuisines["Japanese"]['country_name']}\n
            City: {cuisines["Japanese"]['city']}\n
            Average price of meal for two (U.S. Dollar): {cuisines["Japanese"]['price_dollar']}
            """,
        )

    with brazilian:
        st.metric(
            label=f'Brazilian: {cuisines["Brazilian"]["restaurant_name"]}',
            value=f'{cuisines["Brazilian"]["aggregate_rating"]}/5.0',
            help=f"""
            Country: {cuisines["Brazilian"]['country_name']}\n
            Cidade: {cuisines["Brazilian"]['city']}\n
            Average price of meal for two (U.S. Dollar): {cuisines["Brazilian"]['price_dollar']}
            """,
        )

    return None

    
# ----------------------------
# Configuration
# ----------------------------

st.set_page_config(page_icon=":fork_and_knife:",
                   page_title='Cuisines',
                   layout='wide' # specify how the page content should be laid out =  default is 'centered'
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

# ================================================================================================
#                             Beginning of the code's logical structure
# ================================================================================================

# ----------------------------
# Importing dataset
# ----------------------------
# import file
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
    options=df['country_name'].unique(),
    default=df['country_name'].unique()
)


# enable the filter for countries
selected_rows =  df['country_name'].isin(country)
df = df.loc[selected_rows , :]

st.sidebar.markdown( '''---''' )
st.sidebar.markdown ('###### Powered by Isabela Barbosa')
st.sidebar.markdown ('###### Data Scientist @ Comunidade DS')

#==================================================
# Layout Cuisines Page
#==================================================

st.title( '🍽️Cuisines')

st.markdown( '''---''' )
st.markdown( "## Best Restaurant of the Main Cuisines Types" )

fig = write_metrics( df )
    
    
st.markdown( '''---''' )
with st.container():
    st.subheader('Types of Cuisines')
    text = " ".join(cat for cat in df.cuisines)

    # Ploting Word Cloud
    word_cloud = WordCloud(
        background_color = 'white',
        width=600,
        height=200,
        random_state=1,
        collocations=False,
        stopwords=STOPWORDS,
        ).generate(text)

    # Display the generated Word Cloud
    plt.imshow(word_cloud)
    plt.axis("off")
    fig = plt.show()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot(fig)

    
st.markdown( '''---''' )
with st.container():
    st.subheader('Top 10 Restaurants')
    rest10 = df[['restaurant_name', 'country_name', 'city', 'cuisines', 'price_dollar', 'aggregate_rating', 'votes']].sort_values('aggregate_rating', ascending=False).head(30)
    st.dataframe(rest10)
    