"""Smoke test — verify Azure OpenAI connection and log token usage."""

import os
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()


def get_client() -> AzureOpenAI:
    return AzureOpenAI(
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    )


def test_connection() -> None:
    client = get_client()
    deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[{"role": "user", "content": "Reply with exactly: Azure OpenAI connection successful."}],
            max_tokens=20,
        )
        reply = response.choices[0].message.content
        print(f"[response] {reply}")
        print(
            f"[cost] tokens={response.usage.total_tokens} | "
            f"est_cost=${response.usage.total_tokens / 1_000_000 * 2.50:.6f}"
        )
    except Exception as exc:
        print(f"[error] {exc}")
        raise


if __name__ == "__main__":
    test_connection()
