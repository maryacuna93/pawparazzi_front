import streamlit as st
import requests
import json

st.set_page_config(page_title="🐾 Pawparazzi: Breed Detector!", page_icon="🐶")

st.title("🐾 Pawparazzi: Snap, Upload, Discover!")
st.markdown("""
Welcome to **Pawparazzi**!
Upload a photo of your furry friend and let our magical breed detector reveal their top breeds!
✨ _Unleash the mystery!_ ✨
""")

uploaded_file = st.file_uploader("📸 Upload a pet photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
  st.image(uploaded_file, caption="Your superstar!", use_column_width=True)
  st.write("Analyzing... 🕵️‍♂️🐾")

  files = {"file": uploaded_file.getvalue()}
  try:
    # Replace with your actual API endpoint
    api_url = "https://pawparazziv01-1086583640100.europe-west1.run.app/upload_image"
    response = requests.post(api_url, files=files)
    response.raise_for_status()
    breeds = response.json()
    st.success("✨ Here are the top likely breeds! ✨")
    st.json(breeds)
  except Exception as e:
    st.error(f"Oops! Something went wrong: {e}")
else:
  st.info("Upload a photo to get started! 🐕🐈")
