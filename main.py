import streamlit as st

# Import your page scripts
import Home
import ImageToImage
import TextToImage

PAGES = {
    "Home": Home,
    "Image to Image": ImageToImage,
    "Text to Image": TextToImage
}

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

page = PAGES[selection]
page.app()
