import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
import requests
import io
import altair as alt
import pandas as pd
from toolkit import get_sample_image

# ----- PAGE CONFIG -----
st.set_page_config(
    page_title="Pawparazzi",
    page_icon="🐶",
    layout="wide",
    initial_sidebar_state="collapsed"
)




# ----- HEADER SECTION -----
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://images.unsplash.com/photo-1546421845-6471bdcf3edf?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTUwfHxkb2dzfGVufDB8fDB8fHww")



st.markdown("<h1 style='text-align: center;'>🐾 Pawparazzi</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Can we guess the breed of your dog?</h3>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center;'>
Upload a photo of your furry friend and let our magical breed detector reveal their top breeds!<br>
✨ <em>Unleash the mystery!</em> ✨
</div>
""", unsafe_allow_html=True)
st.markdown("---")

main_columns = st.columns([1,2])
start_run = None
with main_columns[0]:
    # ----- IMAGE UPLOAD -----
    uploaded_file = st.file_uploader("Upload a clear image of your dog 🐕 and use our cropping tool", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        left_top_cols = st.columns([1,1,1,1,1])
        with left_top_cols[2]:
            start_run = st.button("Let's go 📸")
        left_bot_cols = st.columns([1,5,1])
        with left_bot_cols[1]:
            #uploading the image to the streamlit site
            image = Image.open(uploaded_file)
            aspect_ratio = image.width / image.height
            fixed_width = 400
            fixed_height = int(fixed_width / aspect_ratio)
            resized_image = image.resize((fixed_width, fixed_height))
            #cropping the image and displaying it
            cropped_image = st_cropper(
                resized_image,
                default_coords=(10,fixed_width-10,10,fixed_height-10),
                realtime_update=True,
                box_color="#000000"
                )


with main_columns[1]:
    if (uploaded_file is not None) and start_run:
        with st.spinner("Our tiny experts are deliberating 🕵️‍♂️..."):
            #retrieving the image byte data from the cropped image
            img_byte_arr = io.BytesIO()
            cropped_image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            api_url = st.secrets['cloud_api_uri']
            res = requests.post(api_url +"/upload_image", files={'img':img_bytes})

            if res.status_code == 200:
                breeds = res.json()
                sorted_breeds = sorted(
                    ((breed, float(value)) for breed, value in breeds.items()),
                    key=lambda x: x[1],
                    reverse=True
                )

                # ----- RESULTS -----
                top_breed, top_score = sorted_breeds[0]
                if top_score > 0.8:
                    st.markdown(f"🎯 We think your dog is a **{top_breed}** ({top_score * 100:.0f}% confidence)!")
                elif 0.5 < top_score <= 0.8:
                    st.markdown(
                        f"""
                        🤔 Is your dog a **{top_breed}**({top_score * 100:.0f}%)?\n
                        We think it could also be a **{sorted_breeds[1][0]}** ({sorted_breeds[1][1] * 100:.0f}%) or
                        **{sorted_breeds[2][0]}** ({sorted_breeds[2][1] * 100:.0f}%).
                        """)
                elif 0.2 < top_score <= 0.5:
                    st.markdown(f"""
                    🐶 We're not totally sure, but here are our top guesses:
                    - {sorted_breeds[0][0]} ({sorted_breeds[0][1] * 100:.0f}%)
                    - {sorted_breeds[1][0]} ({sorted_breeds[1][1] * 100:.0f}%)
                    - {sorted_breeds[2][0]} ({sorted_breeds[2][1] * 100:.0f}%)
                    """)
                else:
                    st.markdown("""
                    🐶 We are confused... It might be that:
                    - we don't know this breed
                    - there is no dog in the image
                    - the image is blurry or too difficult to understand
                    """)
            else:
                st.error("🐾 Oops, something went wrong. Please try again later.")
                print(res.status_code, res.content)

    if (uploaded_file is not None) and start_run:
        chart_data = pd.DataFrame({
            "Breed": [breed for breed, _ in sorted_breeds[:5]],
            "Confidence": [score for _, score in sorted_breeds[:5]]
        })

        # Create a horizontal bar chart
        bar_chart = alt.Chart(chart_data).mark_bar().encode(
            y=alt.Y("Breed", sort='-x', title="Breed"),   # Vertical axis
            x=alt.X(
                "Confidence",
                title="Confidence Score",
                scale=alt.Scale(domain=[0,1]),
                axis=alt.Axis(format='%')
                ),  # Horizontal axis
            color=alt.value('#D9455B'), #hex code for color bars
            tooltip=["Breed", "Confidence"]
        ).properties(
            width=600,  # Chart width
            height=300  # Chart height
        ).configure_axis(
            labelFontSize=14,
            titleFontSize=16
        )

        relevant_breeds = [(breed, value) for breed, value in sorted_breeds if value > 0.01]
        nb_images = min(len(relevant_breeds), 3)
        columns = st.columns([1 for _ in range(3)])

        sample_images = [get_sample_image(tup[0]) for tup in sorted_breeds[:3]]

        for i in range(nb_images):
            with columns[i]:
                st.image(sample_images[i], caption=f"{sorted_breeds[i][0]}, {sorted_breeds[i][1]* 100:.0f} %", use_container_width=True)
        # ----- BREED CHART -----
        st.markdown("### Confidence by Breed")
        st.altair_chart(bar_chart, use_container_width=True)




# ----- FOOTER -----
st.markdown("""
---
<div style='text-align: center; font-size: 0.9em;'>
Made with ❤️ by the Pawparazzi team
</div>
""", unsafe_allow_html=True)
