import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs
import io

# --- Selenium Imports for Advanced Scraping ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Helper Functions (No changes here) ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def get_actual_url(google_link):
    if "google.com" not in urlparse(google_link).netloc:
        return google_link
    try:
        return parse_qs(urlparse(google_link).query).get('q', [None])[0]
    except Exception:
        return google_link

# --- Scraping Functions (Logic is updated) ---

def scrape_tables_standard(url):
    """Scrapes tables using requests and pandas. Fast but doesn't run JavaScript."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return pd.read_html(response.content)
    except Exception:
        return [] # Return an empty list on any failure

def scrape_tables_advanced(url):
    """
    More robustly scrapes tables using Selenium, explicitly waiting for tables to appear.
    """
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        service = Service(ChromeDriverManager().install())
        with webdriver.Chrome(service=service, options=options) as driver:
            driver.get(url)
            # **KEY IMPROVEMENT**: Wait up to 20 seconds for at least one table to be present.
            # This is much more reliable than a fixed sleep time.
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            html = driver.page_source
        return pd.read_html(html)
    except Exception as e:
        st.error(f"Advanced scraper failed. The site may be heavily protected or have an unusual structure. Error: {e}")
        return []

# --- Streamlit App Interface ---
st.set_page_config(page_title="Smart Web Table Extractor", layout="wide")

st.title("🧠 Smart Web Table Extractor")
st.write("Just paste a URL. The app will automatically find and extract data tables for you.")

# --- Inputs ---
col1, col2 = st.columns([2, 1])
with col1:
    url_input = st.text_input("Enter URL here:", placeholder="https://www.worldometers.info/world-population/")
with col2:
    keyword_input = st.text_input("Filter tables by keyword (optional):", placeholder="e.g., 'country' or 'revenue'")

if url_input:
    actual_url = get_actual_url(url_input)
    if not actual_url:
        st.error("The provided link seems invalid or a valid URL could not be extracted.")
    else:
        st.info(f"Identified destination URL: `{actual_url}`")
        
        with st.spinner("Step 1/2: Trying fast standard scraper..."):
            extracted_tables = scrape_tables_standard(actual_url)

        # --- Automated Fallback Logic ---
        if not extracted_tables:
            st.warning("Standard scraper found no tables. Automatically switching to advanced scraper... (this may take a minute)")
            with st.spinner("Step 2/2: Using advanced scraper to render JavaScript..."):
                extracted_tables = scrape_tables_advanced(actual_url)
        
        # --- Filtering and Display Logic ---
        if extracted_tables:
            # --- Keyword Filtering Logic ---
            filtered_tables = []
            if keyword_input:
                for table_df in extracted_tables:
                    # Check if the keyword exists anywhere in the table's content
                    if keyword_input.lower() in table_df.to_string().lower():
                        filtered_tables.append(table_df)
                if not filtered_tables:
                    st.warning(f"No tables containing the keyword '{keyword_input}' were found.")
                else:
                    st.success(f"Found {len(extracted_tables)} table(s) and filtered down to {len(filtered_tables)} containing '{keyword_input}'.")
            else:
                filtered_tables = extracted_tables # No keyword, so use all tables
                st.success(f"🎉 Found {len(filtered_tables)} table(s) on the page!")

            # --- Display Final Results ---
            for i, table_df in enumerate(filtered_tables):
                with st.expander(f"Table {i+1} (Rows: {len(table_df)}) - Click to view/download"):
                    st.dataframe(table_df)
                    
                    dl_col1, dl_col2 = st.columns(2)
                    with dl_col1:
                        st.download_button(
                            "📥 Download as CSV", table_df.to_csv(index=False).encode('utf-8'),
                            f'table_{i+1}.csv', 'text/csv', key=f'csv_{i}'
                        )
                    with dl_col2:
                        st.download_button(
                            "📄 Download as Excel", to_excel(table_df),
                            f'table_{i+1}.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', key=f'excel_{i}'
                        )
        else:
            st.error("Extraction failed. No tables were found using either scraping method. The website might not contain any HTML tables or may be heavily protected.")