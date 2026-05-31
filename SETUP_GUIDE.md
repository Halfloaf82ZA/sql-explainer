# SQL Explainer — Setup Guide

## What you need before you start

- Python 3.10 or 3.11 installed
- An Azure subscription (free trial is fine)
- Azure OpenAI access approved (apply at aka.ms/oaiapply — takes 1–2 days)
- VS Code or any code editor
- A GitHub account

---

## Step 1 — Get the code

Download and unzip the package, or clone from GitHub:

```bash
git clone https://github.com/Halfloaf82ZA/sql-explainer.git
cd sql-explainer
```

---

## Step 2 — Install dependencies

```bash
pip install -r requirements.txt
```

---

## Step 3 — Set up Azure OpenAI

1. Go to [portal.azure.com](https://portal.azure.com)
2. Create a new Azure OpenAI resource (any region)
3. Go to Azure AI Foundry at [ai.azure.com](https://ai.azure.com)
4. Deploy **gpt-4o** (or gpt-4o-mini for lower cost)
5. Copy your: API key, endpoint URL, and deployment name

---

## Step 4 — Configure your environment

```bash
cp .env.example .env
```

Open `.env` and fill in your Azure OpenAI credentials:

```
AZURE_OPENAI_API_KEY=your-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o
AZURE_OPENAI_API_VERSION=2024-02-01
```

---

## Step 5 — Run the app

```bash
python -m streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Step 6 — Deploy to Streamlit Cloud (optional)

1. Push your repo to GitHub (keep `.env` out — it's in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Add your environment variables as secrets in the Streamlit Cloud dashboard under **Settings → Secrets**:

```toml
AZURE_OPENAI_API_KEY = "your-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
AZURE_OPENAI_DEPLOYMENT = "gpt-4o"
AZURE_OPENAI_API_VERSION = "2024-02-01"
```

---

## Support

Raise an issue on [GitHub](https://github.com/Halfloaf82ZA/sql-explainer/issues).
