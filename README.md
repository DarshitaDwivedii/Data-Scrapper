# 🧠 Smart Web Table Extractor

<p align="center">
  <a href="[YOUR-LIVE-DEMO-URL]">
    <img src="https://img.shields.io/badge/Live-Demo-brightgreen?style=for-the-badge&logo=streamlit" alt="Live Demo">
  </a>
  <a href="https://youtu.be/[YOUR-YOUTUBE-VIDEO-ID]">
    <img src="https://img.shields.io/badge/YouTube-Video_Walkthrough-red?style=for-the-badge&logo=youtube" alt="YouTube Walkthrough">
  </a>
</p>

<p align="center">
  A user-friendly web application built with Streamlit that allows you to extract tabular data from any webpage. This tool is designed to be "smart"—it automatically handles complex websites and can even clean and structure messy data with a single click.
</p>

<p align="center">
  <img src="./assets/app_screenshot.gif" alt="Application Demo GIF" width="80%">
</p>
<p align="center">
  <em>(Suggestion: Create an 'assets' folder in your project and replace the path above with a real screenshot or GIF of your running application)</em>
</p>

---

## 📖 Project Overview

The goal of this project is to create a simple yet powerful tool that eliminates the tedious task of manually copying and pasting data from websites. A user can simply paste a URL, and the application intelligently fetches, parses, and displays all the data tables from that page.

It's built to handle both simple static websites and modern, dynamic sites that load their content using JavaScript. It also includes specialized cleaning routines to handle common cases where data is poorly structured within a single table cell (e.g., book listings on Goodreads).

## ✨ Key Features

*   **Handles Google Search & Direct URLs**: Accepts both direct website URLs and links copied from a Google search results page.
*   **Smart Automated Fallback Scraping**:
    1.  First, it attempts a fast scrape using `requests` and `pandas`.
    2.  If that fails or finds no tables, it **automatically** switches to a powerful advanced scraper using `Selenium` to fully render the page, including JavaScript.
*   **Specialized Post-Scrape Data Cleaning**: Includes an optional one-click cleaning function to parse and structure messy data from sites like Goodreads, turning a single cell of text into multiple, organized columns (Title, Author, Rating, etc.).
*   **Clean, Interactive UI**: Built with Streamlit for a responsive and easy-to-use interface.
*   **One-Click CSV Download**: Download any extracted table as a clean `.csv` file with the click of a button.

## 🚀 Live Demo & Video Walkthrough

*   **Try the app live here:** **[Live Demo Link]** `(<- Replace this with your Streamlit Cloud URL)`
*   **Watch a video walkthrough:** **[YouTube Project Showcase]** `(<- Replace this with your YouTube video link)`

## ⚙️ How It Works

The application follows a logical pipeline to get you the data you need.

1.  **URL Input & Cleaning**: The user provides a URL. The application first checks if it's a `google.com` redirect link and, if so, extracts the true destination URL.

2.  **Attempt 1: Standard Scraping**:
    *   The app sends an HTTP GET request to the URL using the `requests` library. This is very fast.
    *   It then uses `pandas.read_html()` to parse the raw HTML and find all `<table>` elements.
    *   **If tables are found**, the process moves straight to the display step.

3.  **Attempt 2: Advanced Scraping (Automated Fallback)**:
    *   **If the standard scraper finds no tables**, the app assumes the content is loaded dynamically with JavaScript.
    *   It launches a headless Google Chrome browser in the background using `Selenium` and `webdriver-manager`.
    *   It navigates to the URL and intelligently waits for `<table>` elements to become visible on the page.
    *   Once the page is fully rendered, it passes the page source to `pandas.read_html()`.

4.  **Optional Post-Processing (Data Cleaning)**:
    *   If the user has ticked the "Apply book data cleaning" checkbox, the app applies a specific cleaning function to the extracted tables.
    *   This function uses **Regular Expressions (RegEx)** to find and extract patterns (like title, author, ratings) from a messy text cell and splits them into separate, clean columns.

5.  **Display and Download**:
    *   The final, clean DataFrames are displayed in the Streamlit interface using `st.dataframe()`.
    *   Each table is presented within a collapsible `st.expander` to keep the UI tidy.
    *   A download button is provided for each table, allowing the user to save the data as a CSV file.

## 🛠️ Technology Stack

*   **Framework**: [Streamlit](https://streamlit.io/)
*   **Data Manipulation**: [Pandas](https://pandas.pydata.org/)
*   **Standard Scraping**: [Requests](https://requests.readthedocs.io/en/latest/)
*   **Advanced Scraping**: [Selenium](https://www.selenium.dev/)
*   **Driver Management**: [webdriver-manager](https://github.com/SergeyPirogov/webdriver_manager)
*   **HTML Parsing**: [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) & [lxml](https://lxml.de/)
*   **Excel Writing Engine**: [XlsxWriter](https://xlsxwriter.readthedocs.io/)

## 🚀 Setup and Installation

Follow these steps to run the project on your local machine.

#### Prerequisites
*   Python 3.8 - 3.11
*   Google Chrome browser installed (for the advanced Selenium scraper)

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

1.  **Paste a URL** into the input box. This can be a direct link or a link copied from a Google search.
2.  **(Optional) Apply Cleaning:** If you are scraping a book list from a site like **Goodreads** where the title, author, and rating are all in one cell, tick the **"Apply book data cleaning"** checkbox.
3.  **View Results:** The application will automatically perform the scraping. The found tables will appear in collapsible sections.
4.  **Download Data:** Click the "Download as CSV" button under any table to save it to your computer.

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

<p align="center">
  Made with ❤️ by [Your Name]
</p>
<p align="center">
  <a href="https://github.com/[YOUR-GITHUB-USERNAME]">GitHub</a> • 
  <a href="https://www.linkedin.com/in/[YOUR-LINKEDIN-USERNAME]">LinkedIn</a> • 
  <a href="https://twitter.com/[YOUR-TWITTER-USERNAME]">Twitter</a>
</p>