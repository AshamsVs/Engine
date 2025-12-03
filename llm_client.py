import os
import requests

# Correct way: read environment variable by NAME
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
CEREBRAS_API_URL = os.getenv("CEREBRAS_API_URL", "https://api.cerebras.ai/v1/chat/completions")

print("DEBUG: KEY_FROM_PYTHON =", CEREBRAS_API_KEY)

class LLMError(Exception):
    pass


def call_llm(prompt, model="llama3.1-8b", max_tokens=800):
    """
    Sends a prompt to Cerebras Llama-3.1 and returns the response text.
    Includes automatic retry logic for HTTP 429 (rate limit).
    """

    if not CEREBRAS_API_KEY:
        raise LLMError("CEREBRAS_API_KEY is not set.")

    headers = {
        "Authorization": f"Bearer {CEREBRAS_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a highly concise technical documentation generator."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2
    }

    import time
    max_retries = 5
    delay = 3  # seconds between retries

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(CEREBRAS_API_URL, json=payload, headers=headers, timeout=60)

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]

            if response.status_code == 429:
                print(f"[WARN] Rate limit hit (429). Attempt {attempt}/{max_retries}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay += 2
                continue

            raise LLMError(f"Cerebras API error {response.status_code}: {response.text}")

        except requests.exceptions.RequestException:
            print(f"[WARN] Network error on attempt {attempt}. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay += 2

    raise LLMError("Failed after multiple retry attempts.")
