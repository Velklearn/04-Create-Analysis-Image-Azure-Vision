import streamlit as st
import os
from dotenv import load_dotenv
from io import BytesIO

# loading variables from .env file
load_dotenv()

# accessing vision key and endpoint
vision_key = os.getenv("VISION_KEY")
vision_endpoint = os.getenv("VISION_ENDPOINT")

# Quick check that the secrets are loaded — REMOVE these two lines once it works,
# never display an API key in a real app!
# st.text(vision_key)
# st.text(vision_endpoint)
# this is the main function in which we define our webpage
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

# Create the Image Analysis client
client = ImageAnalysisClient(
    endpoint=vision_endpoint,
    credential=AzureKeyCredential(vision_key)
)


def display_analysis_results(result):
    """Display caption and tags from the analysis result."""
    # Caption: a one-sentence description of the image
    if result.caption is not None:
        st.markdown(f"**Caption:** {result.caption.text} "
                    f"(confidence {result.caption.confidence:.2%})")

    # Tags: detected concepts with confidence
    st.markdown("**Tags detected:**")
    if result.tags is not None:
        for tag in result.tags.list:
            st.text(f"'{tag.name}' — confidence {tag.confidence:.2%}")
    else:
        st.text("No tags detected")


def main():
    st.markdown("# Image Analysis App 🖼️")
    st.markdown("### This app allows you to extract visual features from images.")

    # Create tabs for URL and local file analysis
    tab1, tab2 = st.tabs(["Analyse from URL", "Analyse Local Image"])

    # ===== TAB 1: Analyse from URL =====
    with tab1:
        st.subheader("Analyse any image from the web")
        
        image_url = st.text_input(
            "Paste an image URL",
            placeholder="https://example.com/image.jpg",
            label_visibility="collapsed"
        )
        
        if image_url:
            try:
                st.image(image_url, caption="Image to analyse")
                
                if st.button("Analyse image from URL"):
                    with st.spinner("Analysing image..."):
                        result = client.analyze_from_url(
                            image_url=image_url,
                            visual_features=[VisualFeatures.TAGS, VisualFeatures.CAPTION]
                        )
                        display_analysis_results(result)
            except Exception as e:
                st.error(f"Error loading image from URL: {e}")
        else:
            st.info("Enter a URL to an image to get started.")

    # ===== TAB 2: Analyse Local Image =====
    with tab2:
        st.subheader("Analyse a local image")
        
        uploaded_file = st.file_uploader(
            "Upload an image",
            type=["jpg", "jpeg", "png", "gif", "webp"],
            label_visibility="collapsed"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image
            st.image(uploaded_file, caption="Image to analyse")
            
            if st.button("Analyse uploaded image"):
                try:
                    with st.spinner("Analysing image..."):
                        # Read the image data from the uploaded file
                        image_data = uploaded_file.read()
                        
                        # Analyse using the image data
                        result = client.analyze(
                            image_data=image_data,
                            visual_features=[VisualFeatures.TAGS, VisualFeatures.CAPTION]
                        )
                        display_analysis_results(result)
                except Exception as e:
                    st.error(f"Error analysing image: {e}")


# Init code
if __name__ == '__main__':
    main()