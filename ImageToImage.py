import streamlit as st
from PIL import Image


def app():
    st.markdown("<center><h1>AI PHOTO ENHANCER</h1></center>",
                unsafe_allow_html=True)
    st.sidebar.image("logo.jpg")
    # File uploader on the main page
    uploaded_file = st.file_uploader("Upload an Image",
                                     type=["png", "jpg", "jpeg"])

    # Placeholders for layout control
    top_placeholder = st.empty()
    middle_placeholder = st.empty()

    def generate_ai_photo(image):
        # Placeholder function to simulate AI photo generation
        # Replace this with your actual AI model code
        return image

    if uploaded_file is not None:
        # Display the uploaded image at the top
        with top_placeholder:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

        ai_image = None

        # Button to generate AI photo in the middle
        with middle_placeholder:
            if st.button("Generate AI Photo"):
                with st.spinner("Generating..."):
                    ai_image = generate_ai_photo(image)

        # Display images in two columns with labels Before and After
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Before", use_column_width=True)
        with col2:
            if ai_image:
                st.image(ai_image, caption="After", use_column_width=True)
            else:
                st.sidebar.warning("Image not generated")
                st.image(image, caption="After", use_column_width=True)

        # Provide download options
        if ai_image:
            with open("generated_image.png", "rb") as file:
                st.download_button(label="Download Generated Image",
                                   data=file,
                                   file_name="generated_image.png",
                                   mime="image/png")
        else:
            with open(uploaded_file.name, "rb") as file:
                st.download_button(label="Download Uploaded Image",
                                   data=file,
                                   file_name=uploaded_file.name,
                                   mime="image/png")

    else:
        top_placeholder.info("Upload an image to get started.")

    # Footer at the bottom of the sidebar
    st.sidebar.markdown("---")
    st.sidebar.info(
        "**Feedback & Suggestions** [subratasubha2@gmail.com](mailto:subratasubha2@gmail.com)"
    )


if __name__ == "__main__":
    app()
