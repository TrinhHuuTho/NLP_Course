import streamlit as st
from scrpae import scrape_website, split_dom_content, clean_body_content, extract_body_content
from gemini_parser import parse_with_gemini, save_to_csv
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is set
if not os.getenv('GOOGLE_API_KEY'):
    st.error("Please set your GOOGLE_API_KEY in the .env file")
    st.stop()

# Streamlit UI
st.title("AI Web Scraper with Gemini")
st.write("Extract structured data from websites using Google's Gemini AI")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    chunk_size = st.slider("Content Chunk Size", 1000, 5000, 2000)
    output_format = st.selectbox("Output Format", ["CSV", "Excel"])
    
    if st.button("Clear Session"):
        st.session_state.clear()
        st.rerun()

# Main content
url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        with st.spinner("Scraping the website..."):
            # Scrape the website
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the DOM content in Streamlit session state
            st.session_state.dom_content = cleaned_content

            # Display the DOM content in an expandable text box
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
            
            st.success("Website scraped successfully!")

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    st.header("Data Extraction")
    
    # Example prompts
    example_prompts = [
        "Extract all product names and prices",
        "Get all article titles and publication dates",
        "Find all contact information (email, phone, address)"
    ]
    
    selected_prompt = st.selectbox("Choose an example prompt or write your own:", 
                                 ["Custom"] + example_prompts)
    
    if selected_prompt == "Custom":
        parse_description = st.text_area("Describe what data you want to extract")
    else:
        parse_description = selected_prompt

    if st.button("Extract Data"):
        if parse_description:
            with st.spinner("Extracting data..."):
                # Split and parse the content
                dom_chunks = split_dom_content(st.session_state.dom_content, chunk_size)
                df = parse_with_gemini(dom_chunks, parse_description)
                
                if not df.empty:
                    # Display the data
                    st.dataframe(df)
                    
                    # Download options
                    if output_format == "CSV":
                        csv = df.to_csv(index=False)
                        st.download_button(
                            "Download CSV",
                            csv,
                            "extracted_data.csv",
                            "text/csv"
                        )
                    else:
                        excel_buffer = pd.ExcelWriter("extracted_data.xlsx", engine='xlsxwriter')
                        df.to_excel(excel_buffer, index=False)
                        st.download_button(
                            "Download Excel",
                            excel_buffer,
                            "extracted_data.xlsx",
                            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
                else:
                    st.warning("No data found matching your requirements")