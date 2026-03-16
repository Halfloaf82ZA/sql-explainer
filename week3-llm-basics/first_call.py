import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01"),
)


def ask_llm(user_message: str) -> str:
    """Send a message to the LLM and return the text response."""
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[{"role": "user", "content": user_message}],
            max_tokens=500,
        )
        print(
            f"[cost] tokens={response.usage.total_tokens} | "
            f"est_cost=${response.usage.total_tokens / 1_000_000 * 2.50:.6f}"
        )
        return response.choices[0].message.content
    except Exception as exc:
        print(f"[error] {exc}")
        raise


result = ask_llm("What is a SQL JOIN? Explain in 2 sentences.")
print(result)
