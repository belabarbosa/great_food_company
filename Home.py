# -------------------------------------
# Importing libraries
# -------------------------------------
import streamlit as st

from utils import hide_streamlit_style, render_logo, render_footer


st.set_page_config(page_icon="📌",
                   page_title='Home',
                   layout='wide'
)

hide_streamlit_style()


# ----------------------------
# Creating side bar
# ----------------------------

render_logo()
st.sidebar.markdown( '### The place to find your new favorite restaurant!' )
render_footer()


#==================================================
# Layout Home Page
#==================================================

st.write( "# :bar_chart:Great Food Growth Dashboard" )
st.markdown( '''---''' )
st.markdown(
    """
    ### What you are going to find on this dashboard:
    - **Overall:**
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
