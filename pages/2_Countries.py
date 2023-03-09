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


# ----------------------------
# Configuration
# ----------------------------

st.set_page_config(page_icon=":fork_and_knife:", page_title='Countries', layout='wide')
  

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

def restaurants_by_country ( df ):
    df_aux = ( df.loc[:, ['restaurant_id', "country_name"]]
                 .groupby('country_name')
                 .nunique()
                 .sort_values(['restaurant_id'], ascending=False)
                 .reset_index() )

    fig = px.bar(df_aux, x='country_name', y='restaurant_id', text_auto=True, labels={"country_name": " ", "restaurant_id" : " " })
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)' })
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    
    return fig

def cities_by_country ( df ):
    df_aux = ( df.loc[:, ['city', "country_name"]]
                 .groupby('country_name')
                 .nunique()
                 .sort_values(['city'], ascending=False)
                 .reset_index() )
    
    fig = px.treemap(df_aux, path=["country_name"], values='city', color = 'city', color_continuous_scale = 'RdBu',
    template ='plotly_white')
    fig.data[0].texttemplate = "<b>%{label}</b><br> %{value}<br>"
    
    return fig

def avg_reviews_by_country ( df ):
    df_aux = ( np.round(df.loc[:, ['votes', 'country_name']]
                          .groupby('country_name')
                          .mean('votes')
                          .reset_index()
                          .sort_values(['votes'], ascending=False), 2) )
              
    fig = px.bar(df_aux, x="country_name", y="votes", text_auto=True, labels={"country_name": " ", "votes" : " " } )
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)' })
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))

    return fig

def avg_price_meal_for_two_by_country ( df ):
    df_aux = ( df.loc[df['restaurant_name'] != "d'Arry's Verandah Restaurant", ['price_dollar', 'country_name',]]
                 .groupby('country_name')
                 .mean('price_dollar')
                 .sort_values(['price_dollar'], ascending=False)
                 .reset_index() )    
    
    fig = px.bar(df_aux, x="country_name", y="price_dollar", text_auto=True, labels={"country_name": " ", "price_dollar" : " " } )
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)' })
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    
    return fig

def number_of_cuisines_by_country ( df ):
    df_aux = ( df.loc[:, ['cuisines', 'country_name',]]
                 .groupby('country_name')
                 .nunique()
                 .sort_values(['cuisines'], ascending=False)
                 .reset_index() )
    
    fig = px.bar(df_aux, x="country_name", y="cuisines", text_auto=True, labels={"country_name": " ", "cuisines" : " " } )
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)' })
    fig.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
    
    return fig


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

st.title( ':earth_americas:Countries')

st.markdown( '''---''' )
with st.container():
    st.markdown( "## Number of Restaurants Registered")
    fig = restaurants_by_country ( df )
    st.plotly_chart( fig, use_container_width=True )
    

st.markdown( '''---''' )
with st.container():
    st.markdown( "## Number of Cities Registered")
    fig = cities_by_country ( df )
    st.plotly_chart( fig, use_container_width=True )
    
    
st.markdown( '''---''' )    
with st.container():
    st.markdown( "## Average Number of Reviews")
    fig = avg_reviews_by_country ( df )
    st.plotly_chart( fig, use_container_width=True )
    

st.markdown( '''---''' )  
with st.container():
    st.markdown( "## Average Price of a Meal for Two (U.S. Dollar)")
    fig = avg_price_meal_for_two_by_country ( df )
    st.plotly_chart( fig, use_container_width=True )
    
    
st.markdown( '''---''' )
with st.container():
    st.markdown( "## Number of Different Cuisines Available")
    fig = number_of_cuisines_by_country ( df )
    st.plotly_chart( fig, use_container_width=True )