---

### 3. `03-app-py.md`

```md
# Step 3: The Frontend and Agent Workflow

This is the main application file. It contains the Streamlit UI and wires up the Antigravity agent. It includes `nest_asyncio` at the very top to stop Streamlit from crashing during asynchronous operations.

## Instructions
1. Create a file named `app.py` in the same directory as `tools.py`.
2. Paste the following code and save it:

```python
import nest_asyncio
nest_asyncio.apply() # Instantly fixes 'Event loop already running' errors

import streamlit as st
import asyncio
import tempfile
import os
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.content import from_file, from_text

# Import the custom tools built in Step 2
from tools import extract_metadata, generate_ela_heatmap

# 1. UI Window Layout
st.set_page_config(page_title="AI Forensics Dashboard", layout="wide")
st.title("Image Forensics Workspace.")
st.caption("Multimodal AI generation detection via Antigravity SDK.")

# 2. Async Agent Orchestration
async def run_forensic_pipeline(image_path: str):
    # Run deterministic Python backend forensic tools
    metadata = extract_metadata(image_path)
    heatmap_path = generate_ela_heatmap(image_path)
    
    # Bundle data arrays into native Antigravity files
    original_img = from_file(image_path)
    heatmap_img = from_file(heatmap_path)
    meta_text = from_text(f"EXIF Metadata Report:\n{metadata}")
    
    # Define agent configuration and behavior rules
    config = LocalAgentConfig(
        model="gemini-2.5-flash",
        system_instructions="""You are a strict digital forensic analyst. 
        Review the provided original image, the Error Level Analysis (ELA) heatmap, and the metadata text.
        High contrasting edges or scattered noise in the ELA heatmap indicate AI generation or digital modification.
        Conclude explicitly if the image is REAL or AI_GENERATED, followed by bullet points detailing your evidence."""
    )
    
    # Fire off single-shot query
    async with Agent(config) as agent:
        response = await agent.chat([
            "Analyze this evidence payload.", 
            original_img, 
            heatmap_img, 
            meta_text
        ])
        return await response.text(), heatmap_path

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
                report_text, heatmap_file_path = asyncio.run(run_forensic_pipeline(tmp_path))
                
                st.success("Audit Complete")
                st.divider()
                
                # Split dashboard space into two visual zones
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Error Level Analysis")
                    st.image(heatmap_file_path, caption="ELA Heatmap (Bright segments highlight modifications)", use_container_width=True)
                with col2:
                    st.subheader("Agent Forensic Report")
                    st.markdown(report_text)
            except Exception as e:
                st.error(f"Execution failed: {str(e)}")
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)