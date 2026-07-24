# -------------------------------------
# Importing libraries
# -------------------------------------
import pandas as pd
import plotly.express as px
import streamlit as st

from utils import hide_streamlit_style, render_logo, render_footer, render_country_filter


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

st.set_page_config(page_icon=":fork_and_knife:",
                   page_title='Cities',
                   layout='wide'
)

hide_streamlit_style()

# ================================================================================================
#                             Beginning of the code's logical structure
# ================================================================================================

# ----------------------------
# Importing dataset
# ----------------------------
data_source = pd.read_csv('zomato_clean.csv')
df = data_source.copy()


# ----------------------------
# Creating side bar
# ----------------------------

render_logo()
df = render_country_filter(df)
render_footer()


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
