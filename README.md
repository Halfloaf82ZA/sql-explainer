# 🗄️ SQL Explainer

> AI-powered SQL query explainer and optimiser — built with Python, Azure OpenAI, and Streamlit.

---

## What It Does

Paste any SQL query and get back:

- **Plain-English explanation** — every clause broken down, no jargon
- **Optimisation suggestions** — concrete rewrites with explanations
- **Dialect-aware analysis** — T-SQL, PostgreSQL, BigQuery, Snowflake, Generic SQL
- **Copy button** — grab the output as plain text in one click

---

## Who It's For

- Data analysts who work with SQL written by others
- Developers onboarding to a new codebase
- Data engineers reviewing query performance
- Anyone learning SQL who wants clause-by-clause walkthroughs

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| LLM | Azure OpenAI (gpt-4o) |
| UI | Streamlit |
| Language | Python 3.11 |
| Secrets | python-dotenv + Streamlit secrets |
| Deploy | Streamlit Community Cloud |

---

## Running Locally

1. Clone the repo
2. Install: `pip install -r requirements.txt`
3. Copy `.env.example` → `.env` and fill in your Azure OpenAI credentials
4. (Optional) Create `.streamlit/secrets.toml` and add `APP_PASSWORD = "yourpassword"` to enable the password gate
5. Run: `streamlit run app.py`

---

## Project Structure

```
sql-explainer/
├── app.py                  # Streamlit UI
├── llm_client.py           # Azure OpenAI integration
├── requirements.txt
├── .env.example
├── .streamlit/
│   └── secrets.toml        # password gate (never commit)
├── SETUP_GUIDE.md
└── README.md
```

---

## Environment Variables

```
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-01
```

For the optional password gate, set `APP_PASSWORD` in `.streamlit/secrets.toml` (local) or Streamlit Cloud secrets (deployed).

---

*Part of my AI consulting portfolio. Built 2026.*
