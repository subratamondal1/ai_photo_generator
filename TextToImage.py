import os
import io
import warnings
from PIL import Image
import time
import requests
import json
from io import BytesIO

from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import streamlit as st


def generate_with_stabilityai(api=None):
    stability_api = client.StabilityInference(
        key=os.getenv("STABILITY_API_KEY"),
        verbose=True,
    )
    # User inputs for image generation parameters
    default_prompt = """Expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots towering under a blue alien sky, masterful."""
    prompt = st.text_area(
        "Prompt",
        value=default_prompt,
        placeholder=default_prompt,
        help="A detailed description of the image you want to generate.")
    seed = st.sidebar.number_input(
        "Seed",
        value=4253978046,
        step=1,
        help=
        "A number to ensure the image is reproducible. The same seed will generate the same image."
    )
    steps = st.sidebar.number_input(
        "Steps",
        value=50,
        step=1,
        help=
        "The number of steps the model will take to generate the image. More steps usually result in more detailed images."
    )
    cfg_scale = st.sidebar.slider(
        "CFG Scale",
        min_value=1.0,
        max_value=20.0,
        value=8.0,
        step=0.1,
        help=
        "Determines how closely the generated image matches your prompt. Higher values result in closer matches."
    )
    width = st.sidebar.number_input(
        "Width",
        value=1024,
        step=64,
        help="The width of the generated image in pixels.")
    height = st.sidebar.number_input(
        "Height",
        value=1024,
        step=64,
        help="The height of the generated image in pixels.")
    samples = st.sidebar.number_input("Samples",
                                      value=1,
                                      step=1,
                                      help="The number of images to generate.")
    sampler = st.sidebar.selectbox(
        "Sampler",
        options=[
            "ddim", "plms", "k_euler", "k_euler_ancestral", "k_heun",
            "k_dpm_2", "k_dpm_2_ancestral", "k_dpmpp_2s_ancestral", "k_lms",
            "k_dpmpp_2m", "k_dpmpp_sde"
        ],
        index=9,
        help=
        "The algorithm used to denoise the image during generation. Different samplers can produce different styles or qualities."
    )

    sampler_dict = {
        "ddim": generation.SAMPLER_DDIM,
        "k_euler": generation.SAMPLER_K_EULER,
        "k_euler_ancestral": generation.SAMPLER_K_EULER_ANCESTRAL,
        "k_heun": generation.SAMPLER_K_HEUN,
        "k_dpm_2": generation.SAMPLER_K_DPM_2,
        "k_dpm_2_ancestral": generation.SAMPLER_K_DPM_2_ANCESTRAL,
        "k_dpmpp_2s_ancestral": generation.SAMPLER_K_DPMPP_2S_ANCESTRAL,
        "k_lms": generation.SAMPLER_K_LMS,
        "k_dpmpp_2m": generation.SAMPLER_K_DPMPP_2M,
        "k_dpmpp_sde": generation.SAMPLER_K_DPMPP_SDE
    }

    # Initialize session state for managing cancellation
    if "cancel" not in st.session_state:
        st.session_state.cancel = False

    def cancel_generation():
        st.session_state.cancel = True

    generate_button = st.button("Generate Image")
    # cancel_button = st.button("Cancel Generation", on_click=cancel_generation)

    if generate_button:
        st.session_state.cancel = False

        with st.spinner("Generating..."):
            answers = stability_api.generate(prompt=prompt,
                                             seed=seed,
                                             steps=steps,
                                             cfg_scale=cfg_scale,
                                             width=width,
                                             height=height,
                                             samples=samples,
                                             sampler=sampler_dict[sampler])

            for resp in answers:
                if st.session_state.cancel:
                    st.warning("Image generation was cancelled.")
                    break
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTER:
                        st.warning(
                            "Your request was filtered by the safety system.")
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        img = Image.open(io.BytesIO(artifact.binary))
                        st.image(img,
                                 caption="Generated Image",
                                 use_column_width=True)
                        # Save the image to a file
                        img.save("generated_image.png")
                        st.download_button(label="Download Generated Image",
                                           data=img.tobytes(),
                                           file_name="generated_image.png",
                                           mime="image/png")


def generate_with_leonardoai(api_key=None):
    base_url = "https://cloud.leonardo.ai/api/rest/v1"
    api_key = os.getenv("LEONARDO_API_KEY")

    headers = {
        "accept": "application/json",
        "authorization": f"Bearer {api_key}",
        "content-type": "application/json"
    }

    default_prompt = """Expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots towering under a blue alien sky, masterful."""

    prompt = st.text_area(
        "Prompt",
        value=default_prompt,
        placeholder=default_prompt,
        help="A detailed description of the image you want to generate.")

    height = st.sidebar.number_input("Height", value=1024, step=64)
    width = st.sidebar.number_input("Width", value=1024, step=64)

    payload = {
        "height": height,
        "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",
        "prompt": prompt,
        "width": width
    }

    generate_button = st.button("Generate Image")

    if generate_button:
        with st.spinner("Generating..."):
            # Step 1: Initiate image generation
            response = requests.post(f"{base_url}/generations",
                                     headers=headers,
                                     json=payload)

            if response.status_code == 200:
                generation_data = response.json()
                # st.write("Generation initiated:", generation_data)

                generation_id = generation_data["sdGenerationJob"][
                    "generationId"]

                # Step 2: Check generation status and retrieve image URL
                max_attempts = 30
                for attempt in range(max_attempts):
                    status_response = requests.get(
                        f"{base_url}/generations/{generation_id}",
                        headers=headers)

                    if status_response.status_code == 200:
                        status_data = status_response.json()
                        # st.write(f"Generation status (attempt {attempt + 1}):",
                        #          status_data)

                        if status_data["generations_by_pk"][
                                "status"] == "COMPLETE":
                            image_url = status_data["generations_by_pk"][
                                "generated_images"][0]["url"]
                            # st.write("Image URL:", image_url)

                            # Download and display the image
                            image_response = requests.get(image_url)
                            if image_response.status_code == 200:
                                image = Image.open(
                                    BytesIO(image_response.content))
                                st.image(image,
                                         caption="Generated Image",
                                         use_column_width=True)
                            else:
                                st.error("Failed to download the image.")

                            break
                        elif status_data["generations_by_pk"][
                                "status"] == "FAILED":
                            st.error("Image generation failed.")
                            break
                    else:
                        st.error(
                            f"Failed to check generation status: {status_response.status_code}"
                        )
                        break

                    time.sleep(2)  # Wait for 2 seconds before checking again
                else:
                    st.error(
                        "Timed out waiting for image generation to complete.")
            else:
                st.error(
                    f"Failed to initiate generation: {response.status_code}")
                st.text("Response content: " + response.content.decode())
