import streamlit as st
from PIL import Image


def hide_streamlit_style():
    st.markdown(
        """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_logo(width=140):
    image = Image.open('great_food_logo.png')
    st.sidebar.image(image, width=width)


def render_footer():
    st.sidebar.markdown('---')
    st.sidebar.markdown('###### Powered by Isabela Barbosa')
    st.sidebar.markdown('###### Data Scientist @ Comunidade DS')


def render_country_filter(df):
    country = st.sidebar.multiselect(
        "Select the Country:",
        options=df['country_name'].unique().tolist(),
        default=df['country_name'].unique().tolist(),
    )
    selected_rows = df['country_name'].isin(country)
    return df.loc[selected_rows, :]
