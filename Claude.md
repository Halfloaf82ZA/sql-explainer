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
├── .env                  # secrets — never commit
├── .gitignore
├── requirements.txt
├── llm_client.py         # Azure OpenAI calls only
├── app.py                # Streamlit UI only
└── README.md

## Behaviour Rules
- Build features in this order: explain → optimise → copy button → dialect selector
- Suggest the simplest implementation first
- Don't add complexity until the core works
- Production-ready code only — no throwaway snippets
- If a function exceeds 30 lines, suggest splitting it