import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_with_persona(
    system_prompt: str,
    user_message: str,
    temperature: float = 0.3,
    max_tokens: int = 500
) -> str:
    """Call the LLM with a system prompt defining its role."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

# Test 1: SQL expert persona
sql_system = """You are a senior data engineer with 15 years of experience.
Explain SQL concepts clearly and concisely. Use plain English.
Always mention performance implications where relevant."""

result = ask_with_persona(
    system_prompt=sql_system,
    user_message="Explain what a clustered index is."
)
print("=== SQL Expert ===")
print(result)

# Test 2: Same question, different temperature
result_creative = ask_with_persona(
    system_prompt=sql_system,
    user_message="Explain what a clustered index is.",
    temperature=1.2  # more random
)
print("\n=== High Temperature ===")
print(result_creative)