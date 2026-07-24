# -------------------------------------
# Importing libraries
# -------------------------------------
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

from utils import hide_streamlit_style, render_logo, render_footer, render_country_filter

# ----------------------------
# Configuration
# ----------------------------

st.set_page_config(page_icon=":fork_and_knife:",
                   page_title='Overall',
                   layout='wide'
)

hide_streamlit_style()

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
data_source = pd.read_csv('zomato_clean.csv')
df = data_source.copy()


# ----------------------------
# Creating side bar
# ----------------------------

render_logo()
df = render_country_filter(df)
render_footer()

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
        col1.metric( 'Registered Countries',  number_of_countries )

    with col2:
        number_of_cities = df['city'].nunique()
        col2.metric( 'Registered Cities',  number_of_cities)

    with col3:
        registered_restaurants = (f"{df['restaurant_id'].nunique():,}".replace(',', ','))
        col3.metric( 'Registered Restaurants', registered_restaurants )

    with col4:
        number_of_cuisines = df['cuisines'].nunique()
        col4.metric( 'Types of Cuisines', number_of_cuisines )

    with col5:
        sum_votes = df['votes'].sum()
        votes = (f"{sum_votes:,}".replace(',', ','))
        col5.metric('Reviews Received', value=votes)


st.markdown( '''---''' )
with st.container():
    st.markdown( "## Check the map below to find Great Food locations 🗺️" )
    create_map(df)
