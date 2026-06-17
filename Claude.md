# SQL Explainer — Claude Code Instructions

## Project
Python + Azure OpenAI + Streamlit app that explains SQL queries in plain English.
Phase 0 portfolio project. Keep it simple and shippable.

## Stack
- Python
- Azure OpenAI SDK (openai package, AzureOpenAI client)
- Streamlit for UI
- python-dotenv for secrets

## Environment
Secrets live in .env — never hardcode them. Never commit .env.
Required env vars:
- AZURE_OPENAI_API_KEY
- AZURE_OPENAI_ENDPOINT
- AZURE_OPENAI_DEPLOYMENT (currently: gpt-4o)
- AZURE_OPENAI_API_VERSION (use: 2024-02-01)

## Code Standards
- Modular functions — keep llm_client.py separate from app.py
- Error handling on every API call — wrap in try/except
- After every Azure OpenAI API call, log token usage and cost:
  print(f"[cost] tokens={response.usage.total_tokens} | est_cost=${response.usage.total_tokens / 1_000_000 * 2.50:.6f}")
- Clear variable names — no single letter variables
- Type hints on all functions

## File Structure
sql-explainer/
├── .env                    # secrets — never commit
├── .env.example            # template for local setup
├── .gitignore
├── .streamlit/
│   └── secrets.toml        # Streamlit Cloud secrets (never commit)
├── requirements.txt
├── llm_client.py           # Azure OpenAI calls only
├── app.py                  # Streamlit UI only
├── SETUP_GUIDE.md          # local setup walkthrough
├── README.md
├── hello_streamlit.py      # scratch / learning file
├── prompt_patterns.py      # prompt engineering experiments
├── system_messages.py      # system prompt drafts
├── test_azure.py           # manual Azure OpenAI connection test
└── week3-llm-basics/       # course exercises — not part of the app

## Auth & Rate Limiting
- Password gate via `st.secrets["APP_PASSWORD"]` — set in `.streamlit/secrets.toml` locally and in Streamlit Cloud secrets for deployment
- Session rate limit: 10 requests per session, enforced in `app.py`

## Behaviour Rules
- All planned features are shipped: explain, optimise, dialect selector, copy button, password gate, rate limiting
- Suggest the simplest implementation first
- Don't add complexity until the core works
- Production-ready code only — no throwaway snippets
- If a function exceeds 30 lines, suggest splitting it