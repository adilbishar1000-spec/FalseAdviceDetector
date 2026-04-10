def offline_reason(text):
    text = text.lower()

    if "stop" in text or "replace" in text or "quit" in text:
        return "🚨 Dangerous: Stopping prescribed treatment may cause serious harm."

    if "cure" in text or "detox" in text or "guarantee" in text:
        return "⚠️ Misleading: This makes unverified cure or detox claims."

    return "✅ Safe: General health advice without harmful medical claims."
