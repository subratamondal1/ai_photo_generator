import streamlit as st
from PIL import Image

# Set the page title, layout, and custom favicon
st.set_page_config(page_title="AI PHOTO GENERATOR",
                   page_icon="🤖",
                   layout="wide")

# App title
st.markdown("<center><h1>🤖 AI PHOTO GENERATOR</h1></center>",
            unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Settings")
st.sidebar.markdown("Configure your AI Photo Generator settings here.")

# File uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload an Image",
                                         type=["png", "jpg", "jpeg"])

# Placeholder for the main content
placeholder = st.empty()


def generate_ai_photo(image):
    return image


if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    placeholder.image(image, caption="Uploaded Image", use_column_width=True)

    # Button to generate AI photo
    if st.button("Generate AI Photo"):
        with st.spinner("Generating..."):
            ai_image = generate_ai_photo(image)
            col1, col2 = st.columns(2)

            with col1:
                st.image(image,
                         caption="Original Image",
                         use_column_width=True)

            with col2:
                st.image(ai_image,
                         caption="AI Generated Photo",
                         use_column_width=True)

            st.success("AI Photo Generated Successfully!")

else:
    placeholder.info("Upload an image to get started.")

# Footer
st.sidebar.markdown("---")
st.sidebar.info(
    "Developed by [**Subrata Mondal**](mailto:subrata@thealgohype.com?subject=Feedback%20%26%20Suggestions)"
)
