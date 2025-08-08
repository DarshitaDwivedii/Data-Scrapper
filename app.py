import streamlit as st
import pandas as pd
from urllib.parse import urlparse, parse_qs
import requests
import re # Import the regular expressions library

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Core Helper & Scraping Functions (Unchanged) ---
def get_actual_url(google_link):
    if "google.com" not in urlparse(google_link).netloc: return google_link
    try: return parse_qs(urlparse(google_link).query).get('q', [None])[0]
    except Exception: return google_link

def scrape_tables_standard(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return pd.read_html(response.content)
    except Exception: return []

def scrape_tables_advanced(url):
    try:
        options = Options(); options.add_argument("--headless"); options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage"); options.add_argument("--window-size=1920,1080")
        service = Service(ChromeDriverManager().install())
        with webdriver.Chrome(service=service, options=options) as driver:
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            html = driver.page_source
        return pd.read_html(html)
    except Exception as e:
        st.error(f"Advanced scraper failed. Error: {e}"); return []

# --- Streamlit App Interface ---
st.set_page_config(page_title="Smart Web Table Extractor", layout="wide")
st.title("🧠 Smart Web Table Extractor")
st.write("Paste a URL to extract tables, then use the advanced RegEx tool to clean and structure your data.")

# Initialize session state for storing original and cleaned tables
if 'extracted_tables' not in st.session_state:
    st.session_state.extracted_tables = []
if 'cleaned_table' not in st.session_state:
    st.session_state.cleaned_table = None

url_input = st.text_input("Enter URL here:", placeholder="https://www.goodreads.com/list/show/1.Best_Books_Ever")

if st.button("Extract Tables"):
    # Clear all previous results before starting a new extraction
    st.session_state.extracted_tables = []
    st.session_state.cleaned_table = None
    actual_url = get_actual_url(url_input)
    if not actual_url:
        st.error("Invalid URL.")
    else:
        st.info(f"Identified destination URL: `{actual_url}`")
        with st.spinner("Step 1/2: Trying fast standard scraper..."):
            tables = scrape_tables_standard(actual_url)
        if not tables:
            st.warning("Standard scraper found no tables. Switching to advanced scraper...")
            with st.spinner("Step 2/2: Using advanced scraper..."):
                tables = scrape_tables_advanced(actual_url)
        
        st.session_state.extracted_tables = tables
        if not tables:
            st.error("Extraction failed. No tables were found.")
        else:
            st.success(f"🎉 Success! Found {len(st.session_state.extracted_tables)} raw table(s).")


# --- DISPLAY ORIGINAL TABLES ---
if st.session_state.extracted_tables:
    st.markdown("---")
    st.header("Raw Extracted Tables")
    st.write("These are the tables exactly as they were found on the webpage.")
    for i, table_df in enumerate(st.session_state.extracted_tables):
        with st.expander(f"Raw Table {i+1} (Rows: {len(table_df)})", expanded=False):
            st.dataframe(table_df)
            st.download_button(
                "📥 Download Raw CSV", table_df.to_csv(index=False).encode('utf-8'),
                f'raw_table_{i+1}.csv', 'text/csv', key=f'raw_csv_{i}'
            )

    # --- DYNAMIC DATA CLEANING UI (REGULAR EXPRESSION EXTRACTOR) ---
    st.markdown("---")
    st.header("Interactive Data Cleaning: The RegEx Extractor")
    st.write("Select a raw table and a column, then provide a RegEx pattern to extract data into new, clean columns.")
    
    table_index = st.selectbox(
        "Select a raw table to clean:", 
        options=range(len(st.session_state.extracted_tables)),
        format_func=lambda i: f"Raw Table {i+1}",
        key='table_selector'
    )
    
    # Use a copy of the selected table for cleaning operations
    selected_df = st.session_state.extracted_tables[table_index].copy()
    
    column_to_parse = st.selectbox(
        "1. Select the column with the messy data:",
        options=selected_df.columns,
        key='column_selector'
    )
    
    st.markdown("""
    **2. Define Your Extraction Patterns (using Regular Expressions)**
    
    A RegEx pattern finds and extracts data from text. Each part you want to extract into a new column should be a **named capture group** like `(?P<Name>...)`.
    
    * **Need help building a RegEx?** Check out [**Regex101.com**](https://regex101.com/) - it's an excellent interactive tool.
    """)

    goodreads_example = r"^(?P<Title>.*?)\s+\(.*by\s+(?P<Author>.*?)\s+(?P<Avg_Rating>\d+\.\d+)\s+avg rating.*score:\s+(?P<Score>[\d,]+)"
    
    regex_pattern = st.text_area(
        "Enter your RegEx pattern here:",
        value=goodreads_example,
        height=150,
        key='regex_input'
    )
    
    if st.button("Apply Extraction", key='apply_button'):
        if not regex_pattern:
            st.warning("Please enter a RegEx pattern.")
        else:
            try:
                # Use str.extract to apply the regex pattern
                extracted_data = selected_df[column_to_parse].astype(str).str.extract(regex_pattern)
                
                if extracted_data.dropna(how='all').empty:
                    st.error("Extraction failed. Your RegEx pattern did not match any data in the selected column. Please check your pattern on Regex101.")
                    st.session_state.cleaned_table = None
                else:
                    st.success("Extraction successful! See the cleaned table result below.")
                    remaining_df = selected_df.drop(columns=[column_to_parse])
                    cleaned_df = pd.concat([remaining_df, extracted_data], axis=1)
                    # Store the newly cleaned table in session state
                    st.session_state.cleaned_table = cleaned_df
            
            except re.error as e:
                st.error(f"Invalid Regular Expression: {e}. Please check your pattern syntax.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")

# --- DISPLAY CLEANED TABLE RESULT ---
if st.session_state.cleaned_table is not None:
    st.markdown("---")
    with st.expander("✨ Cleaned Table Result", expanded=True):
        st.dataframe(st.session_state.cleaned_table)
        st.download_button(
            "✅ Download Cleaned CSV", st.session_state.cleaned_table.to_csv(index=False).encode('utf-8'),
            f'cleaned_table.csv', 'text/csv', key='cleaned_csv'
        )