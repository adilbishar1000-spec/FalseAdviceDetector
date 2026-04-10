import google.generativeai as genai

# ✅ Configure API Key
genai.configure(api_key="YOUR_API_KEY_HERE")

# ✅ Updated Gemini Model (Correct One)
model = genai.GenerativeModel("gemini-1.5-flash")


def chatbot_response(prompt, classification=None):
    """
    Generates response from Gemini AI.
    If Gemini fails, returns token/quota exceeded message.
    """

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        # ✅ Custom fallback message
        return "⚠️ Gemini tokens/quota exceeded. Offline explanation shown instead."
