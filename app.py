import streamlit as st
from PIL import Image
import requests

st.set_page_config(
    page_title="Pawparazzi",
    page_icon="🐶"
    )

st.title("🐾 Pawparazzi: Can we guess the breed of your dog?")
st.markdown("""
Welcome to **Pawparazzi**!
Upload a photo of your furry friend and let our magical breed detector reveal their top breeds!
✨ _Unleash the mystery!_ ✨
""")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(Image.open(uploaded_file), caption="Your superstar!")

    with st.spinner("Our tiny experts are deliberating 🕵️‍♂️..."):

        img_bytes = uploaded_file.getvalue()
        api_url = st.secrets['cloud_api_uri']
        res = requests.post(api_url +"/upload_image", files={'img':img_bytes})

        if res.status_code == 200:
            breeds = res.json()
            sorted_breeds=sorted(
                ((breed, float(value)) for breed, value in breeds.items()),
                key=lambda x: float(x[1]),
                reverse=True
                )
            if sorted_breeds[0][1] > 0.8:
                st.success(f"""
                           We think your dog is a {sorted_breeds[0][0]}.
                           We're {sorted_breeds[0][1]*100:.3}% sure about it
                           """)
            elif 0.8 > sorted_breeds[0][1] > 0.5:
                st.success(f"""
                           Is your dog a {sorted_breeds[0][0]} ({sorted_breeds[0][1]*100:.3}%)?
                           We think it could also be {sorted_breeds[1][0]} ({sorted_breeds[1][1]*100:.3}%) or {sorted_breeds[2][0]} ({sorted_breeds[2][1]*100:.3}%).
                           """)
            else:
                st.success(f"""We're not sure but is it a {sorted_breeds[0][0]} ({sorted_breeds[0][1]*100:.3}%),
                           {sorted_breeds[1][0]} ({sorted_breeds[1][1]*100:.3}%) or {sorted_breeds[2][0]} ({sorted_breeds[2][1]*100:.3}%)?
                           """)

        else:
            st.markdown("Oops, something went wrong")
            print(res.status_code, res.content)
