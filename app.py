import streamlit as st
import requests
import pandas as pd
from urllib.parse import urlparse, parse_qs
import io
import re # Import the regular expressions library

# --- Selenium Imports for Advanced Scraping ---
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- Helper Functions (URL and Scraping logic is unchanged) ---
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
        options = Options()
        options.add_argument("--headless"); options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage"); options.add_argument("--window-size=1920,1080")
        service = Service(ChromeDriverManager().install())
        with webdriver.Chrome(service=service, options=options) as driver:
            driver.get(url)
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "table")))
            html = driver.page_source
        return pd.read_html(html)
    except Exception as e:
        st.error(f"Advanced scraper failed. Error: {e}")
        return []

# --- NEW: Data Cleaning Function for Book Data ---
def clean_book_data(df):
    """
    Specifically processes a DataFrame from a site like Goodreads.
    It splits the combined 'Title/Author/Rating' column into multiple clean columns.
    """
    # Check if the dataframe has a column that contains the combined book data
    # We assume it's the second column (index 1) for Goodreads lists.
    if len(df.columns) < 2:
        return df # Not the format we expect, return as is

    target_col_name = df.columns[1]
    
    # Use regular expressions to extract each piece of data.
    # We wrap this in a function to apply to each row.
    def parse_book_cell(cell_text):
        if not isinstance(cell_text, str):
            return {} # Return empty dict if cell is not text

        title = re.search(r'^(.*?)\s*\(', cell_text)
        author = re.search(r'by\s(.*?)\s*(\d+\.\d+ avg rating)', cell_text)
        avg_rating = re.search(r'(\d+\.\d+)\s*avg rating', cell_text)
        total_ratings = re.search(r'—\s*([\d,]+)\s*ratings', cell_text)
        score = re.search(r'score:\s*([\d,]+)', cell_text)
        voters = re.search(r'and\s*([\d,]+)\s*people voted', cell_text)
        
        # Build a dictionary of the extracted data, cleaning it up
        data = {
            'Title': title.group(1).strip() if title else None,
            'Author': author.group(1).strip() if author else None,
            'Avg Rating': float(avg_rating.group(1)) if avg_rating else None,
            'Total Ratings': int(total_ratings.group(1).replace(',', '')) if total_ratings else None,
            'Score': int(score.group(1).replace(',', '')) if score else None,
            'Voters': int(voters.group(1).replace(',', '')) if voters else None,
        }
        return data

    # Apply the parsing function to the target column and create a new DataFrame from the results
    parsed_data = df[target_col_name].apply(parse_book_cell).apply(pd.Series)
    
    # Combine the new parsed data with the original DataFrame (dropping the old messy column)
    cleaned_df = pd.concat([df.drop(columns=[target_col_name]), parsed_data], axis=1)
    
    return cleaned_df


# --- Streamlit App Interface ---
st.set_page_config(page_title="Smart Web Table Extractor", layout="wide")

st.title("🧠 Smart Web Table Extractor")
st.write("Paste a URL to automatically find and extract tables. For sites like Goodreads, use the cleaning option to structure the data.")

# --- Inputs ---
url_input = st.text_input("Enter URL here:", placeholder="Try a list from Goodreads.com")

# --- NEW: Optional cleaning checkbox ---
apply_cleaning = st.checkbox("Apply book data cleaning (for sites like Goodreads)")

if url_input:
    actual_url = get_actual_url(url_input)
    if not actual_url:
        st.error("Invalid URL.")
    else:
        st.info(f"Identified destination URL: `{actual_url}`")
        with st.spinner("Step 1/2: Trying fast standard scraper..."):
            extracted_tables = scrape_tables_standard(actual_url)

        if not extracted_tables:
            st.warning("Standard scraper found no tables. Switching to advanced scraper...")
            with st.spinner("Step 2/2: Using advanced scraper..."):
                extracted_tables = scrape_tables_advanced(actual_url)
        
        if extracted_tables:
            st.success(f"🎉 Found {len(extracted_tables)} table(s) on the page!")
            
            # --- Processing and Display Logic ---
            final_tables = []
            for df in extracted_tables:
                # If checkbox is ticked, try to clean the dataframe
                if apply_cleaning:
                    final_tables.append(clean_book_data(df))
                else:
                    final_tables.append(df)

            for i, table_df in enumerate(final_tables):
                with st.expander(f"Table {i+1} (Rows: {len(table_df)}) - Click to view/download"):
                    st.dataframe(table_df)
                    # --- SIMPLIFIED: Only CSV download button ---
                    st.download_button(
                        "📥 Download as CSV", table_df.to_csv(index=False).encode('utf-8'),
                        f'table_{i+1}.csv', 'text/csv', key=f'csv_{i}'
                    )
        else:
            st.error("Extraction failed. No tables were found.")