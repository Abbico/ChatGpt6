
import streamlit as st
from PIL import Image
import os

# Set page config
st.set_page_config(page_title="DAJANIII Pro", layout="wide")

# Load and display logo
logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, width=200)

# Main UI
st.title("📊 DAJANIII Pro - Stock Trading Assistant")
st.markdown("Welcome to your intelligent portfolio assistant powered by OpenRouter AI and real-time financial data.")
st.info("Upload a PDF portfolio to begin...")

# Upload section
uploaded_file = st.file_uploader("Upload PDF Portfolio", type=["pdf"])
if uploaded_file:
    st.success("PDF uploaded. Portfolio parsing will be available in the full app release.")

# Add main() function for Streamlit to call
def main():
    st.write("🚀 App is running successfully.")

# Ensure main is called
if __name__ == "__main__":
    main()
