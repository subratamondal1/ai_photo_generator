import streamlit as st
from PIL import Image


def app():
    st.markdown("<center><h1>AI PHOTO ENHANCER X GENERATOR</h1></center>",
                unsafe_allow_html=True)
    st.info(
        "Welcome to the multi-page AI Photo Generator app. Use the navigation on the left to select a page."
    )
    st.sidebar.image("logo.jpg")
