import nest_asyncio
nest_asyncio.apply()  # Instantly fixes 'Event loop already running' errors

from dotenv import load_dotenv
load_dotenv()  # Auto-load API key from .env file

import streamlit as st
import asyncio
import tempfile
import os
from google import genai
from google.genai import types
from PIL import Image

# Import the custom tools built in Step 2
from tools import extract_metadata, generate_ela_heatmap

# --- Configure Gemini ---
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY)

# 1. UI Window Layout
st.set_page_config(page_title="AI Forensics Dashboard", layout="wide")
st.title("Image Forensics Workspace.")
st.caption("Multimodal AI generation detection via Gemini SDK.")

SYSTEM_INSTRUCTION = """You are a strict digital forensic analyst. 
Review the provided original image, the Error Level Analysis (ELA) heatmap, and the metadata text.
High contrasting edges or scattered noise in the ELA heatmap indicate AI generation or digital modification.
Conclude explicitly if the image is REAL or AI_GENERATED, followed by bullet points detailing your evidence."""


# 2. Async Agent Orchestration
async def run_forensic_pipeline(image_path: str):
    # Run deterministic Python backend forensic tools
    metadata = extract_metadata(image_path)
    heatmap_path = generate_ela_heatmap(image_path)

    # Read image bytes for Gemini multimodal input
    with open(image_path, "rb") as f:
        original_bytes = f.read()
    with open(heatmap_path, "rb") as f:
        heatmap_bytes = f.read()

    contents = [
        types.Part.from_text(text="Analyze this evidence payload."),
        types.Part.from_bytes(data=original_bytes, mime_type="image/png"),
        types.Part.from_bytes(data=heatmap_bytes, mime_type="image/png"),
        types.Part.from_text(text=f"EXIF Metadata Report:\n{metadata}"),
    ]

    def _call():
        return client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )

    response = await asyncio.to_thread(_call)
    return response.text, heatmap_path


# 3. Streamlit App Rendering
uploaded_file = st.file_uploader("Upload target image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Original Uploaded Image", width=400)

    if st.button("Run Security Audit", use_container_width=True):
        with st.spinner("Analyzing structural noise grids..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                # Trigger the async process safely
                report_text, heatmap_file_path = asyncio.run(
                    run_forensic_pipeline(tmp_path)
                )

                st.success("Audit Complete")
                st.divider()

                # Split dashboard space into two visual zones
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Error Level Analysis")
                    st.image(
                        heatmap_file_path,
                        caption="ELA Heatmap (Bright segments highlight modifications)",
                        use_container_width=True
                    )
                with col2:
                    st.subheader("Agent Forensic Report")
                    st.markdown(report_text)
            except Exception as e:
                st.error(f"Execution failed: {str(e)}")
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
