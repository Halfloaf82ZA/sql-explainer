# SQL Explainer

An AI-powered tool that explains SQL queries in plain English and suggests performance optimisations.

Built with Python, Azure OpenAI (gpt-4o), and Streamlit.

## What it does

- Paste any SQL query (T-SQL, PostgreSQL, BigQuery)
- Get a structured plain-English explanation broken down by clause
- Get concrete optimisation suggestions with rewritten SQL where applicable

## Live demo

[Link to deployed app]

## Tech stack

- Python 3.11
- Azure OpenAI API (gpt-4o)
- Streamlit
- python-dotenv

## Running locally

1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your Azure OpenAI credentials
4. Run: `streamlit run app.py`

## Environment variables
