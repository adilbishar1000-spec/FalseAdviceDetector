import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("\n✅ AVAILABLE MODELS:\n")

for m in genai.list_models():
    print(m.name, " | supports:", m.supported_generation_methods)
