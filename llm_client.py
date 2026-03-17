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

def explain_sql(sql_query: str, dialect: str = "Generic SQL") -> str:
    """Explain a SQL query in plain English, with dialect-aware analysis."""
    if not sql_query.strip():
        return "No SQL query provided."
    system_prompt = f"""You are a senior data engineer with deep expertise in {dialect}.

Explain the provided SQL query in plain English.
Break down each clause (SELECT, FROM, WHERE, JOIN, GROUP BY, HAVING, ORDER BY) separately.
Use bullet points for each clause.
Highlight any {dialect}-specific syntax or functions.
Use simple language — the reader is a business analyst, not a DBA.
Identify any potential performance concerns specific to {dialect}."""
    try:
        response = _client.chat.completions.create(
            model=_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Explain this {dialect} query:\n\n{sql_query}"}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        result = response.choices[0].message.content
        print(f"[cost] tokens={response.usage.total_tokens} | est_cost=${response.usage.total_tokens / 1_000_000 * 2.50:.6f}")
        return result
    except Exception as e:
        return f"Error calling Azure OpenAI: {e}"

def optimise_sql(sql_query: str, dialect: str = "Generic SQL") -> str:
    """Suggest optimisations for a SQL query, with dialect-aware suggestions."""
    if not sql_query.strip():
        return "No SQL query provided."
    system_prompt = f"""You are a senior data engineer and query performance expert specialising in {dialect}.

Analyse the provided SQL query for performance issues and suggest concrete improvements.
For each suggestion:
1. Explain the problem
2. Explain why it matters in {dialect} specifically
3. Provide the rewritten SQL where applicable

Focus on: index usage, join order, predicate pushdown, unnecessary columns in SELECT, subquery vs CTE trade-offs.
If the query looks well-optimised, say so explicitly."""
    try:
        response = _client.chat.completions.create(
            model=_DEPLOYMENT,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Optimise this {dialect} query:\n\n{sql_query}"}
            ],
            temperature=0.2,
            max_tokens=1000
        )
        result = response.choices[0].message.content
        print(f"[cost] tokens={response.usage.total_tokens} | est_cost=${response.usage.total_tokens / 1_000_000 * 2.50:.6f}")
        return result
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