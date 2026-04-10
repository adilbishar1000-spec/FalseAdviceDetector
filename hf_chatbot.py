import requests

HF_TOKEN = ""
API_URL = "https://router.huggingface.co/v1/chat/completions"

def hf_explain(text):

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "zai-org/GLM-4.7-Flash:novita",
        "messages": [
            {
                "role": "user",
                "content": f"In 2 sentences, why is this health advice dangerous or misleading? {text}"
            }
        ],
        "max_tokens": 500
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            message = response.json()["choices"][0]["message"]

            # This model puts response in reasoning_content, not content
            reply = message.get("content") or message.get("reasoning_content", "")

            # Extract just the final answer from reasoning_content
            if "reasoning_content" in message and not message.get("content"):
                lines = message["reasoning_content"].strip().split("\n")
                # Get last non-empty lines as the conclusion
                reply = " ".join(
                    line.strip("* ").strip()
                    for line in lines
                    if line.strip() and not line.strip().startswith(("1.", "2.", "3.", "*", "-"))
                )
                if not reply:
                    reply = message["reasoning_content"][-300:]

            return reply.strip() or "No explanation returned."

        elif response.status_code == 401:
            return "❌ Invalid token. Regenerate at huggingface.co/settings/tokens"

        elif response.status_code == 403:
            return "❌ Token lacks permission. Use 'Read' access token."

        elif response.status_code == 503:
            return "⏳ Model loading, try again in 20 seconds."

        else:
            return f"⚠️ AI unavailable (Status {response.status_code}): {response.text[:200]}"

    except requests.exceptions.Timeout:
        return "⏱️ Request timed out. Try again shortly."

    except requests.exceptions.RequestException as e:
        return f"🔌 Connection error: {str(e)}"