import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SQL_QUERY = """
SELECT
    c.customer_name,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount) AS lifetime_value
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.created_date >= DATEADD(year, -1, GETDATE())
GROUP BY c.customer_name
HAVING COUNT(o.order_id) > 5
ORDER BY lifetime_value DESC
"""

def call_llm(system: str, user: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        temperature=0.2,
        max_tokens=800
    )
    return response.choices[0].message.content


# Pattern 1: Zero-shot — just ask
zero_shot = call_llm(
    system="You are a senior data engineer. Explain SQL queries in plain English.",
    user=f"Explain this query:\n{SQL_QUERY}"
)
print("=== Zero-Shot ===")
print(zero_shot)


# Pattern 2: Few-shot — show examples first
few_shot_system = """You are a senior data engineer. Explain SQL queries in plain English.

Example:
Query: SELECT COUNT(*) FROM orders WHERE status = 'open'
Explanation: Counts how many orders currently have an open status.

Query: SELECT customer_id, MAX(order_date) FROM orders GROUP BY customer_id
Explanation: Finds each customer's most recent order date.

Now explain the following query in the same style:"""

few_shot = call_llm(
    system=few_shot_system,
    user=f"Query:\n{SQL_QUERY}"
)
print("\n=== Few-Shot ===")
print(few_shot)


# Pattern 3: Chain-of-thought — ask it to reason step by step
cot_system = """You are a senior data engineer.
When explaining SQL queries, think through it step by step:
1. What tables are involved?
2. What joins are happening and why?
3. What filtering is applied?
4. What aggregation or grouping occurs?
5. What does the final result set look like?"""

cot = call_llm(
    system=cot_system,
    user=f"Explain this query:\n{SQL_QUERY}"
)
print("\n=== Chain-of-Thought ===")
print(cot)