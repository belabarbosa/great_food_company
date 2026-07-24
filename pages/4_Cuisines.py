# -------------------------------------
# Importing libraries
# -------------------------------------
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

from utils import hide_streamlit_style, render_logo, render_footer, render_country_filter


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

    italian, american, arabian, japanese, brazilian = st.columns(len(cuisines))

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

    with japanese:
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
            City: {cuisines["Brazilian"]['city']}\n
            Average price of meal for two (U.S. Dollar): {cuisines["Brazilian"]['price_dollar']}
            """,
        )

    return None


# ----------------------------
# Configuration
# ----------------------------

st.set_page_config(page_icon=":fork_and_knife:",
                   page_title='Cuisines',
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
# Layout Cuisines Page
#==================================================

st.title( '🍽️Cuisines')

st.markdown( '''---''' )
st.markdown( "## Best Restaurant of the Main Cuisines Types" )

write_metrics( df )


st.markdown( '''---''' )
with st.container():
    st.subheader('Types of Cuisines')
    text = " ".join(cat for cat in df.cuisines)

    # Plotting the word cloud
    word_cloud = WordCloud(
        background_color = 'white',
        width=600,
        height=200,
        random_state=1,
        collocations=False,
        stopwords=STOPWORDS,
        ).generate(text)

    fig, ax = plt.subplots()
    ax.imshow(word_cloud)
    ax.axis("off")
    st.pyplot(fig)


st.markdown( '''---''' )
with st.container():
    st.subheader('Top 10 Restaurants')
    rest10 = df[['restaurant_name', 'country_name', 'city', 'cuisines', 'price_dollar', 'aggregate_rating', 'votes']].sort_values('aggregate_rating', ascending=False).head(30)
    st.dataframe(rest10)
