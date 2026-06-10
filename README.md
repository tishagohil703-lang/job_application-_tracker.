# Job Application Tracker

A modern job application tracking dashboard built with Streamlit, SQLite, Pandas, and Plotly.

## Project Structure

- `app.py` - Main Streamlit application.
- `database.py` - SQLite database utility for job CRUD operations.
- `charts.py` - Plotly chart definitions for analytics.
- `requirements.txt` - Python package dependencies.
- `jobs.db` - SQLite database file.

## Features

- Dashboard with total applications, interviews, offers, rejections, and success rate.
- Job management with add, edit, delete, search, and status filters.
- Analytics charts for monthly applications, status distribution, top companies, and interview conversion.
- Clean sidebar navigation and responsive layout.

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Plotly

## Setup

1. Open a terminal in the project folder:
   ```bash
   cd "C:\Users\Tisha gohil\job_application_tracker"
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

## Run the app

1. Start Streamlit:
   ```bash
   streamlit run app.py
   ```
2. Open the local URL shown in the terminal.

## Notes

- The application uses a local SQLite database file named `jobs.db`.
- If `jobs.db` does not exist, it will be created automatically when the app first runs.
- If Python is not found, install Python and ensure it is available in your system PATH.
