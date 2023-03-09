# -------------------------------------
# Importing libraries
# -------------------------------------
import pandas as pd
import plotly.express as px
import seaborn as se
import numpy as np
from haversine import haversine
import inflection
from PIL import Image
import streamlit as st


# -------------------------------------
# Functions
# -------------------------------------

def top_best_restaurants( df ):
    df_aux = ( df.loc[df['aggregate_rating'] > 4 , ['restaurant_id', 'city', 'country_name']]
      .groupby('city')
      .count()
      .sort_values(['restaurant_id'], ascending=False)
      .reset_index()
      .head(10) )
    
    fig = px.bar(df_aux, x='city', y='restaurant_id', color='country_name', text_auto=True, labels={"city": " ", "restaurant_id" : "Number of Restaurants", "country_name" : "Country Name"})  
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)' })
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    return fig
    
    
def top_worse_restaurants( df ):
    df_aux = ( df.loc[df['aggregate_rating'] < 2.5 , ['restaurant_id', 'city']]
                  .groupby('city')
                  .count()
                  .sort_values(['restaurant_id'], ascending=False)
                  .reset_index()
                  .head(10) )
    
    fig = px.bar(df_aux, x='city', y='restaurant_id', text_auto=True, labels={"city": " ", "restaurant_id" : "Number of Restaurants" })
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)' })
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    return fig

def distinct_cuisines (df):
    df_aux = ( df.loc[:, ['cuisines', 'city']]
                 .groupby('city')
                 .nunique()
                 .sort_values(['cuisines'], ascending=False)
                 .reset_index()
                 .head(10) )
    
    fig = px.bar(df_aux, x='city', y='cuisines', text_auto=True, labels={"city": " ", "cuisines" : "Number of Cuisines" })
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)' })
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    
    return fig


# ----------------------------
# Configuration
# ----------------------------

st.set_page_config(page_icon=":fork_and_knife:", # icone da pagina
                   page_title='Cities', # titulo da pagina
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
# Layout Countries Page
#==================================================

st.title( ':cityscape: Cities')

st.markdown( '''---''' )
with st.container():
    st.markdown( "## Top 10 Cities With Restaurants Rated Above 4")
    fig = top_best_restaurants ( df )
    st.plotly_chart( fig, use_container_width=True )
    

st.markdown( '''---''' )
with st.container():
    st.markdown( "## Top 10 Cities With Restaurants Rated Below 2.5")
    fig = top_worse_restaurants ( df )
    st.plotly_chart( fig, use_container_width=True )
              

st.markdown( '''---''' )
with st.container():
    st.markdown( "## Top 10 Cities With the Most Different Types of Cuisine")
    fig = distinct_cuisines ( df )
    st.plotly_chart( fig, use_container_width=True )