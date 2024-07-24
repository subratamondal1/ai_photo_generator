from io import BytesIO
import IPython
import json
import os
from PIL import Image
import requests
import time

# Access Secret Key
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")


def send_generation_request(
    host,
    params,
):
  headers = {
      "Accept": "image/*",
      "Authorization": f"Bearer {STABILITY_API_KEY}"
  }

  # Encode parameters
  files = {}
  image = params.pop("image", None)
  mask = params.pop("mask", None)
  if image is not None and image != '':
    files["image"] = open(image, 'rb')
  if mask is not None and mask != '':
    files["mask"] = open(mask, 'rb')
  if len(files) == 0:
    files["none"] = ''

  # Send request
  print(f"Sending REST request to {host}...")
  response = requests.post(host, headers=headers, files=files, data=params)
  if not response.ok:
    raise Exception(f"HTTP {response.status_code}: {response.text}")

  return response


def send_async_generation_request(
    host,
    params,
):
  headers = {
      "Accept": "application/json",
      "Authorization": f"Bearer {STABILITY_KEY}"
  }

  # Encode parameters
  files = {}
  if "image" in params:
    image = params.pop("image")
    files = {"image": open(image, 'rb')}

  # Send request
  print(f"Sending REST request to {host}...")
  response = requests.post(host, headers=headers, files=files, data=params)
  if not response.ok:
    raise Exception(f"HTTP {response.status_code}: {response.text}")

  # Process async response
  response_dict = json.loads(response.text)
  generation_id = response_dict.get("id", None)
  assert generation_id is not None, "Expected id in response"

  # Loop until result or timeout
  timeout = int(os.getenv("WORKER_TIMEOUT", 500))
  start = time.time()
  status_code = 202
  while status_code == 202:
    response = requests.get(
        f"{host}/result/{generation_id}",
        headers={
            **headers, "Accept": "image/*"
        },
    )

    if not response.ok:
      raise Exception(f"HTTP {response.status_code}: {response.text}")
    status_code = response.status_code
    time.sleep(10)
    if time.time() - start > timeout:
      raise Exception(f"Timeout after {timeout} seconds")

  return response


def generate_ai_photo(image):
  return image

def backend
prompt = "dark red high contrast render of a psychedelic tree of life illuminating dust in a mystical cave with red background." #@param {type:"string"}
negative_prompt = "" #@param {type:"string"}
aspect_ratio = "3:2" #@param ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]
seed = 0 #@param {type:"integer"}
output_format = "png" #@param ["webp", "jpeg", "png"]

host = f"https://api.stability.ai/v2beta/stable-image/generate/ultra"

params = {
    "prompt" : prompt,
    "negative_prompt" : negative_prompt,
    "aspect_ratio" : aspect_ratio,
    "seed" : seed,
    "output_format": output_format
}

response = send_generation_request(
    host,
    params
)

# Decode response
output_image = response.content
finish_reason = response.headers.get("finish-reason")
seed = response.headers.get("seed")

# Check for NSFW classification
if finish_reason == 'CONTENT_FILTERED':
    raise Warning("Generation failed NSFW classifier")

# Save and display result
generated = f"generated_{seed}.{output_format}"
with open(generated, "wb") as f:
    f.write(output_image)
print(f"Saved image {generated}")

output.no_vertical_scroll()
print("Result image:")
IPython.display.display(Image.open(generated))
