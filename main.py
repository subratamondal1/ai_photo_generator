import os
import grpc

import streamlit as st

from TextToImage import generate_with_stabilityai, generate_with_leonardoai
from stability_sdk import client

st.markdown("<center><h1>AI PHOTO GENERATOR</h1></center>",
            unsafe_allow_html=True)
st.sidebar.image("logo.jpg")

st.sidebar.header("Configurations:")

# Initialize the Stability API client
stability_api = client.StabilityInference(
    key=os.getenv("STABILITY_API_KEY"),
    verbose=True,
)

option = st.selectbox("**Generate with:**", ("StabilityAI", "LeonardoAI"))

if option == "StabilityAI":
  try:
    api = st.text_input("**Enter your StabilityAI API Key [Optional]**",
                        type="password",
                        help="Provide your API key to access the service.")
    if api:
      generate_with_stabilityai(api=api)
    else:
      generate_with_stabilityai(api=stability_api)
  except grpc.RpcError as e:
    if e.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
      st.warning(
          "Your organization does not have enough balance to request this action. Please provide a valid API key."
      )
    else:
      st.error(f"An error occurred: {e.details()}")
else:
  try:
    api = st.text_input("**Enter your LeonardoAI API Key [Optional]**",
                        type="password",
                        help="Provide your API key to access the service.")
    if api:
      generate_with_leonardoai(api_key=api)
    else:
      generate_with_leonardoai(api_key=os.getenv("LEONARDO_API_KEY"))
  except grpc.RpcError as e:
    if e.code() == grpc.StatusCode.RESOURCE_EXHAUSTED:
      st.warning(
          "Your organization does not have enough balance to request this action. Please provide a valid API key."
      )
    else:
      st.error(f"An error occurred: {e.details()}")

# Footer
st.sidebar.markdown("---")
st.sidebar.info("Feedback & Suggestions subrata@thealgohype.com")
