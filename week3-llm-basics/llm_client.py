import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
)

_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

_SQL_EXPLAIN_SYSTEM = """You are a senior data engineer with deep SQL expertise.
Explain SQL queries in plain English, structured as follows:

1. **Purpose** — What does this query do in one sentence?
2. **Clause breakdown** — Explain each clause (SELECT, FROM, JOIN, WHERE, GROUP BY, ORDER BY) separately.
3. **Performance notes** — Flag any potential issues (missing indexes, SELECT *, large scans, etc.)
4. **Dialect** — Identify the SQL dialect if possible (T-SQL, PostgreSQL, BigQuery, etc.)

Use clear, simple language. Assume the reader is a business analyst, not a DBA."""

_SQL_OPTIMISE_SYSTEM = """You are a senior data engineer specialising in query optimisation.
Given a SQL query, suggest concrete improvements:

1. **Indexing recommendations** — what indexes would help?
2. **Rewrite suggestions** — is there a more efficient way to write this?
3. **Potential issues** — identify any anti-patterns (SELECT *, implicit conversions, correlated subqueries, etc.)
4. **Estimated impact** — rough assessment of improvement expected

Be specific and actionable. Show rewritten SQL where applicable."""

def explain_sql(sql_query: str) -> str:
    """Explain a SQL query in plain English."""
    if not sql_query.strip():
        return "No SQL query provided."
    try:
        response = _client.chat.completions.create(
            model=_DEPLOYMENT,
            messages=[
                {"role": "system", "content": _SQL_EXPLAIN_SYSTEM},
                {"role": "user", "content": f"Explain this SQL query:\n\n{sql_query}"}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling Azure OpenAI: {e}"

def optimise_sql(sql_query: str) -> str:
    """Suggest optimisations for a SQL query."""
    if not sql_query.strip():
        return "No SQL query provided."
    try:
        response = _client.chat.completions.create(
            model=_DEPLOYMENT,
            messages=[
                {"role": "system", "content": _SQL_OPTIMISE_SYSTEM},
                {"role": "user", "content": f"Optimise this SQL query:\n\n{sql_query}"}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling Azure OpenAI: {e}"

if __name__ == "__main__":
    test_query = """
    SELECT c.name, COUNT(o.id) as orders, SUM(o.total) as revenue
    FROM customers c
    JOIN orders o ON c.id = o.customer_id
    WHERE o.created_at > '2024-01-01'
    GROUP BY c.name
    ORDER BY revenue DESC
    """
    print("=== EXPLAIN ===")
    print(explain_sql(test_query))
    print("\n=== OPTIMISE ===")
    print(optimise_sql(test_query))