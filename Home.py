import streamlit as st
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

main_columns = st.columns([1,1])
with main_columns[0]:
    # ----- IMAGE UPLOAD -----
    uploaded_file = st.file_uploader("Upload a clear image of your dog 🐕", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        aspect_ratio = image.width / image.height
        fixed_width = 400
        fixed_height = int(fixed_width / aspect_ratio)
        resized_image = image.resize((fixed_width, fixed_height))
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(resized_image, caption="📸 Your superstar!", use_container_width=False)

with main_columns[1]:
    if uploaded_file is not None:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        with st.spinner("Our tiny experts are deliberating 🕵️‍♂️..."):
            img_bytes = uploaded_file.getvalue()
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
                    st.success(f"🎯 We think your dog is a **{top_breed}** ({top_score * 100:.2f}% confidence)!")
                elif 0.5 < top_score <= 0.8:
                    st.markdown(f"""
                        <div style="background-color:#fff3cd; padding:15px; border-left:5px solid #ffeeba; border-radius:8px;">
                            <strong>🤔 Is your dog a <span style="color:#856404;">{top_breed}</span> ({top_score * 100:.2f}%)?</strong><br>
                            We also suspect <strong>{sorted_breeds[1][0]}</strong> ({sorted_breeds[1][1] * 100:.2f}%) or
                            <strong>{sorted_breeds[2][0]}</strong> ({sorted_breeds[2][1] * 100:.2f}%).
                        </div>
                    """, unsafe_allow_html=True)
                elif 0.2 < top_score <= 0.5:
                    st.info(f"""
                    🐶 We're not totally sure, but here are our top guesses:
                    - {sorted_breeds[0][0]} ({sorted_breeds[0][1] * 100:.2f}%)
                    - {sorted_breeds[1][0]} ({sorted_breeds[1][1] * 100:.2f}%)
                    - {sorted_breeds[2][0]} ({sorted_breeds[2][1] * 100:.2f}%)
                    """)
                else:
                    st.info(f"""
                    🐶 We are confused... It might be that\n
                        - we don't know this breed\n
                        - there is no dog in the image\n
                        - the image is blurry or too difficult to understand
                    """)



                chart_data = pd.DataFrame({
                    "Breed": [breed for breed, _ in sorted_breeds[:5]],
                    "Confidence": [score for _, score in sorted_breeds[:5]]
                })

                # Create a horizontal bar chart
                bar_chart = alt.Chart(chart_data).mark_bar().encode(
                    y=alt.Y("Breed", sort='-x', title="Breed"),   # Horizontal axis
                    x=alt.X("Confidence", title="Confidence Score"),  # Vertical axis
                    tooltip=["Breed", "Confidence"]
                ).properties(
                    width=600,  # Chart width
                    height=300  # Chart height
                ).configure_axis(
                    labelFontSize=14,
                    titleFontSize=16
                )

                relevant_breeds = [(breed, value) for breed, value in sorted_breeds if value > 0.1]
                nb_images = min(len(relevant_breeds), 3)
                columns = st.columns([1 for _ in range(3)])

                sample_images = [get_sample_image(tup[0]) for tup in sorted_breeds[:3]]

                for i in range(nb_images):
                    with columns[i]:
                        st.image(sample_images[i], caption=f"{sorted_breeds[i]}", use_container_width=True)
                # ----- BREED CHART -----
                st.markdown("### Confidence by Breed")
                st.altair_chart(bar_chart, use_container_width=True)



            else:
                st.error("🐾 Oops, something went wrong. Please try again later.")
                print(res.status_code, res.content)





# ----- FOOTER -----
st.markdown("""
---
<div style='text-align: center; font-size: 0.9em;'>
Made with ❤️ by the Pawparazzi team
</div>
""", unsafe_allow_html=True)
