import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="About", page_icon="📖")

st.title("📖 About Pawparazzi")
st.markdown("""
Welcome to **Pawparazzi**! 🐾

This app helps you identify your dog’s breed using machine learning...""")

BREEDS_DIR = "breeds_sample_images"

image_files = [
    f for f in os.listdir(BREEDS_DIR)
    if f.lower().endswith((".png", ".jpg", ".jpeg"))
]

breed_dict = {
    os.path.splitext(f)[0].replace("_", " ").title(): f
    for f in image_files
}

ALL_BREEDS = sorted(breed_dict.keys())

st.markdown("Use the search box below to check if your dog’s breed is supported:")

search_term = st.text_input("Search for a breed", placeholder="Type here...")

filtered = [
    breed for breed in ALL_BREEDS
    if search_term.lower() in breed.lower()
]

if search_term:
    if filtered:
        st.success(f"Found {len(filtered)} match(es):")
        for breed in filtered:
            st.markdown(f"### {breed}")
            image_path = os.path.join(BREEDS_DIR, breed_dict[breed])
            st.image(Image.open(image_path), width=300, caption=f"Sample of {breed}")
    else:
        st.warning("❌ No matching breed found.")


show_list = st.checkbox("Show full list of recognizable breeds")

if show_list:
    for breed in ALL_BREEDS:
        with st.expander(breed):
            image_path = os.path.join(BREEDS_DIR, breed_dict[breed])
            st.image(Image.open(image_path), caption=f"Sample of {breed}", use_container_width=True)


("""
### 👩‍💻 Built by:
- [Maria Alejandra Acuña](https://github.com/maryacuna93)
- [Maria Englert](https://github.com/mariaenglert)
- [Hadrien Pulcini](https://github.com/hadulc)
- [Robin Rölz](https://github.com/rroelz)
""")
