import streamlit as st
from google import genai
from PIL import Image

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

def get_gemini_response(input_text, image, prompt):

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            f"{prompt}\nArtifact Name: {input_text}",
            image
        ]
    )

    return response.text


st.set_page_config(page_title="Gemini Historical Artifact Description")

st.header("🏺 Gemini Historical Artifact Description App")

input_text = st.text_input("Enter Artifact Name:")

uploaded_file = st.file_uploader(
    "Choose an image of an artifact...",
    type=["jpg", "jpeg", "png"]
)

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("🚀 Generate Artifact Description")

input_prompt = """
You are a professional historian.

Give a detailed artifact description including:

- Name
- Origin
- Time Period
- Historical Significance
- Cultural Importance
- Interesting Facts

Explain clearly in structured points.
"""

if submit:

    if image is None:
        st.error("Please upload an image.")
    else:
        try:
            result = get_gemini_response(
                input_text,
                image,
                input_prompt
            )

            st.subheader("📜 Description of the Artifact:")
            st.write(result)

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
