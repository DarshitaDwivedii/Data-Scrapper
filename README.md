# 🧠 Smart Web Table Extractor

<p align="center">
  <a href="[YOUR-LIVE-DEMO-URL]">
    <img src="https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
  <a href="https://youtu.be/[YOUR-YOUTUBE-VIDEO-ID]">
    <img src="https://img.shields.io/badge/YouTube-Video_Walkthrough-red?style=for-the-badge&logo=youtube" alt="YouTube Walkthrough">
  </a>
</p>

> ### 🚧 **Development Status: Active & Evolving** 🚧
> This project is under active development. The core scraping functionality is stable, but new features for data cleaning and transformation are being added and refined. User feedback is highly welcome!

<p align="center">
  A user-friendly web application built with Streamlit that allows you to extract tabular data from any webpage. This tool is designed to be "smart"—it automatically handles complex websites and now includes interactive tools to clean and restructure your data using the power of Regular Expressions.
</p>

<!-- <p align="center">
  <img src="./assets/app_screenshot.gif" alt="Application Demo GIF" width="80%">
</p>
<p align="center">
  <em>(Suggestion: Create an 'assets' folder in your project and replace the path above with a real screenshot or GIF of your running application)</em>
</p> -->

---

## 📖 Project Overview

The goal of this project is to create a simple yet powerful tool that eliminates the tedious task of manually copying and pasting data from websites. A user can simply paste a URL, and the application intelligently fetches, parses, and displays all the raw data tables from that page.

The real power comes from the post-scraping toolkit. It's built to handle both simple static websites and modern, dynamic sites that load their content using JavaScript. Crucially, it includes an **interactive RegEx Extractor** that lets the user extract and separate multiple pieces of information from a single messy column into a new, perfectly structured table.

## ✨ Key Features

*   **Handles All Link Types**: Accepts both direct website URLs and links copied from a Google search results page.
*   **Smart Automated Fallback Scraping**:
    1.  First, it attempts a fast scrape using `requests` and `pandas`.
    2.  If that fails, it **automatically** switches to a powerful `Selenium` scraper to fully render the page, including JavaScript.
*   **Interactive RegEx Extractor**: The core cleaning feature allows you to:
    *   Select any raw table and any column containing messy data.
    *   Write a **Regular Expression (RegEx)** to define extraction patterns.
    *   Use **named capture groups** `(?P<Name>...)` to automatically create and name new columns.
    *   Instantly see the cleaned "after" table for review and download.
*   **Clear Before-and-After View**: The app keeps the raw extracted tables visible for comparison while showing the newly cleaned table in a separate section.
*   **Clean, Interactive UI**: Built with Streamlit for a responsive and easy-to-use interface.
*   **One-Click CSV Download**: Download both the original raw tables and your final cleaned table as `.csv` files.

## 🚀 Live Demo & Video Walkthrough

*   **Try the app live here:** **[Live Demo Link]** `(<- Replace this with your Streamlit Cloud URL)`
*   **Watch a video walkthrough:** **[YouTube Project Showcase]** `(<- Replace this with your YouTube video link)`

## ⚙️ How It Works

The application follows a logical pipeline to get you the data you need.

1.  **URL Input & Scraping**: A user provides a URL. The app automatically detects the link type and uses its two-stage (standard then advanced) scraping mechanism to fetch all tables from the page.

2.  **Display Raw Results**: All tables found on the page are immediately displayed in collapsible sections, showing the data exactly as it appeared on the website.

3.  **Interactive Cleaning with RegEx**:
    *   The user selects a raw table and a specific column they wish to clean.
    *   They provide a RegEx pattern in the text area. This pattern defines what data to "pull out." For example, to get a book title and author, the pattern would describe how to find the text for the title and how to find the text for the author.
    *   Using **named capture groups** (e.g., `(?P<Title>...)` and `(?P<Author>...)`) in the RegEx tells the app to create new columns named `Title` and `Author`.

4.  **Display Cleaned Result**:
    *   Upon applying the extraction, a new "Cleaned Table Result" appears.
    *   This new table contains the original columns (minus the messy one) plus the new, cleanly extracted columns. The raw table remains unchanged for comparison.

5.  **Download**: The user can download either the original raw tables or the final, structured table as CSV files.

## 🛠️ Technology Stack

*   **Framework**: [Streamlit](https://streamlit.io/)
*   **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
*   **Regular Expressions**: Python's built-in `re` module
*   **Standard Scraping**: [Requests](https://requests.readthedocs.io/en/latest/)
*   **Advanced Scraping**: [Selenium](https://www.selenium.dev/)
*   **Driver Management**: [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager)
*   **HTML Parsing**: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) & [lxml](https://lxml.de/)

## 🚀 Setup and Installation

Follow these steps to run the project on your local machine.

#### Prerequisites
*   Python 3.8 - 3.11
*   Google Chrome browser installed (required for the advanced Selenium scraper)

#### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/[YOUR-GITHUB-USERNAME]/[YOUR-REPOSITORY-NAME].git
    cd [YOUR-REPOSITORY-NAME]
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    # For Windows
    python -m venv .venv
    .venv\Scripts\activate

    # For macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install the required libraries from the `requirements.txt` file:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    Your web browser will automatically open with the application running. The first time you use the app, `webdriver-manager` may take a moment to download the correct browser driver for Selenium. This is a one-time process.

## 🧑‍💻 How to Use the App

1.  **Paste a URL** into the input box and click "Extract Tables."
2.  **Inspect the Raw Tables** that appear below. Identify a table and a specific column that needs cleaning.
3.  **Go to the "Interactive Data Cleaning" tool.**
    *   Select the raw table and the messy column from the dropdown menus.
    *   Write a RegEx pattern in the text area to define what data to extract. Use `(?P<ColumnName>...)` to create new, named columns. An example for Goodreads is provided by default.
4.  **Click "Apply Extraction."**
5.  **View and Download:** A new "Cleaned Table Result" will appear. You can view it and download it as a clean CSV file.

