import os

import pickle
from flask import Flask, request
from dotenv import load_dotenv

load_dotenv()

from hf_chatbot import hf_explain
from offline_reason import offline_reason
from similarity_matcher import find_best_match

app = Flask(__name__)

# ===============================
# Load ML Model
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
vectorizer = pickle.load(open(os.path.join(BASE_DIR, "vectorizer.pkl"), "rb"))

# ===============================
# Prediction Function
# ===============================
def predict(text):
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    confidence = max(model.predict_proba(vec)[0]) * 100

    if pred == 0:
        return "✅ Safe Advice", confidence, "success"
    elif pred == 1:
        return "⚠️ Misleading Advice", confidence, "warning"
    else:
        return "🚨 Dangerous Advice", confidence, "danger"


# ===============================
# Main Route
# ===============================
@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    confidence = None
    color = None

    matched_text = None
    reason = None
    safe_tip = None
    similarity_score = None

    offline_exp = None
    chatbot_reply = None

    if request.method == "POST":

        advice = request.form.get("advice")

        # Prediction
        result, confidence, color = predict(advice)

        # Similarity match
        match = find_best_match(advice)

        if match:
            matched_text = match.get("matched_text")
            reason = match.get("reason")
            safe_tip = match.get("safe_tip")
            similarity_score = match.get("score")
        else:
            reason = "No myth match found."
            safe_tip = "Consult a medical professional."
            matched_text = "N/A"
            similarity_score = 0.0

        # Offline explanation
        offline_exp = offline_reason(advice)

        # AI explanation ONLY for risky advice
        if "Dangerous" in result or "Misleading" in result:
            chatbot_reply = hf_explain(advice)
        else:
            chatbot_reply = "✅ Safe advice detected. AI explanation skipped."

    # ===============================
    # HTML UI
    # ===============================
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Health Myth Analyzer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        body {{
            background: url('https://images.unsplash.com/photo-1579684385127-1ef15d508118?q=80&w=2080&auto=format&fit=crop') no-repeat center center fixed;
            background-size: cover;
            font-family: 'Inter', sans-serif;
            color: #333;
        }}
        .glass-panel {{
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        }}
        .gradient-text {{
            background: linear-gradient(135deg, #2563eb, #14b8a6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .card-hover {{
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .card-hover:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
        }}
        .loader {{
            border-top-color: #2563eb;
            -webkit-animation: spinner 1.5s linear infinite;
            animation: spinner 1.5s linear infinite;
        }}
        @keyframes spinner {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .fade-in {{
            animation: fadeIn 0.6s ease-out forwards;
        }}
    </style>
</head>
<body class="min-h-screen flex items-center justify-center p-4 sm:p-8">

<div class="w-full max-w-4xl glass-panel rounded-3xl p-6 sm:p-10 shadow-2xl relative overflow-hidden">
    <!-- Decorative Blob -->
    <div class="absolute top-0 right-0 -mr-20 -mt-20 w-64 h-64 rounded-full bg-blue-400 opacity-20 blur-3xl"></div>
    <div class="absolute bottom-0 left-0 -ml-20 -mb-20 w-64 h-64 rounded-full bg-teal-400 opacity-20 blur-3xl"></div>

    <div class="text-center relative z-10 mb-8">
        <h2 class="text-4xl font-extrabold mb-2 gradient-text"><i class="fa-solid fa-notes-medical mr-2"></i> Health Myth Analyzer</h2>
        <p class="text-gray-500 text-sm">Powered by Machine Learning & Free AI (GPT-4 via g4f)</p>
    </div>

    <form method="POST" class="relative z-10 mb-8" onsubmit="document.getElementById('loading').classList.remove('hidden'); document.getElementById('results').classList.add('hidden');">
        <div class="flex flex-col sm:flex-row gap-3">
            <div class="relative flex-grow">
                <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <i class="fa-solid fa-magnifying-glass text-gray-400"></i>
                </div>
                <input type="text" name="advice" 
                       class="w-full pl-11 pr-4 py-4 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-sm text-lg transition-shadow"
                       placeholder="Enter health advice (e.g. Drinking bleach cures infections...)"
                       required>
            </div>
            <button type="submit" class="bg-gradient-to-r from-blue-600 to-teal-500 hover:from-blue-700 hover:to-teal-600 text-white font-bold py-4 px-8 rounded-xl shadow-lg transition-all transform hover:scale-105 flex items-center justify-center gap-2">
                <span>Analyze</span>
                <i class="fa-solid fa-wand-magic-sparkles"></i>
            </button>
        </div>
    </form>

    <div id="loading" class="hidden text-center py-12 z-10 relative">
        <div class="inline-block w-12 h-12 border-4 border-gray-200 rounded-full loader mb-4"></div>
        <p class="text-blue-600 font-semibold text-lg animate-pulse">Analyzing medical advice with AI...</p>
    </div>

    {"" if result is None else f"""
    <div id="results" class="relative z-10 fade-in">
        <div class="mb-8 text-center p-6 rounded-2xl {'bg-green-100 text-green-800 border border-green-200' if color == 'success' else 'bg-yellow-100 text-yellow-800 border border-yellow-200' if color == 'warning' else 'bg-red-100 text-red-800 border border-red-200'} shadow-sm">
            <h3 class="text-3xl font-bold mb-2 flex items-center justify-center gap-2">
                <i class="fa-solid {'fa-circle-check' if color == 'success' else 'fa-triangle-exclamation' if color == 'warning' else 'fa-skull-crossbones'}"></i> 
                {result}
            </h3>
            <span class="inline-block px-3 py-1 bg-white bg-opacity-50 rounded-full text-sm font-semibold shadow-sm backdrop-blur-sm">
                AI Confidence: {confidence:.2f}%
            </span>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <div class="col-span-1 md:col-span-2 card-hover bg-white rounded-xl p-5 border-l-4 border-blue-400 shadow-sm">
                <h4 class="font-bold text-gray-700 mb-2 flex items-center gap-2"><i class="fa-solid fa-bullseye text-blue-500"></i> Closest Myth Match</h4>
                <p class="text-gray-600 italic mb-2">"{matched_text}"</p>
                <div class="w-full bg-gray-200 rounded-full h-2.5">
                  <div class="bg-blue-500 h-2.5 rounded-full" style="width: {min(100, similarity_score * 100)}%"></div>
                </div>
                <p class="text-xs text-right text-gray-500 mt-1">Similarity Score: {similarity_score:.2f}</p>
            </div>

            <div class="card-hover bg-white rounded-xl p-5 border-l-4 border-red-400 shadow-sm">
                <h4 class="font-bold text-gray-700 mb-2 flex items-center gap-2"><i class="fa-solid fa-circle-exclamation text-red-500"></i> Why It's Risky</h4>
                <p class="text-gray-600 text-sm leading-relaxed">{reason}</p>
            </div>

            <div class="card-hover bg-white rounded-xl p-5 border-l-4 border-green-400 shadow-sm">
                <h4 class="font-bold text-gray-700 mb-2 flex items-center gap-2"><i class="fa-solid fa-heart-pulse text-green-500"></i> Safe Alternative</h4>
                <p class="text-gray-600 text-sm leading-relaxed">{safe_tip}</p>
            </div>

            <div class="col-span-1 md:col-span-2 card-hover bg-white rounded-xl p-5 border-l-4 border-purple-500 shadow-sm">
                <h4 class="font-bold text-gray-700 mb-2 flex items-center gap-2"><i class="fa-solid fa-robot text-purple-500"></i> Free AI Deep Dive</h4>
                <p class="text-gray-600 text-sm leading-relaxed">{chatbot_reply}</p>
            </div>
            
            <div class="col-span-1 md:col-span-2 card-hover bg-white rounded-xl p-5 border-l-4 border-orange-400 shadow-sm">
                <h4 class="font-bold text-gray-700 mb-2 flex items-center gap-2"><i class="fa-solid fa-book-medical text-orange-500"></i> Offline Knowledge Base</h4>
                <p class="text-gray-600 text-sm leading-relaxed">{offline_exp}</p>
            </div>

        </div>
    </div>
    """}

    <div class="mt-8 pt-4 border-t border-gray-200 text-center relative z-10">
        <p class="text-xs text-gray-400">
            <i class="fa-solid fa-scale-balanced mr-1"></i> For educational purposes only. Always consult a licensed healthcare professional for medical advice.
        </p>
        <p class="text-xs text-gray-400 mt-2 opacity-75 font-medium tracking-wide">
            Created by bishar & team
        </p>
    </div>

</div>

</body>
</html>
"""


# ===============================
# Run App
# ===============================
if __name__ == "__main__":
    token = os.getenv("HF_TOKEN")
    print("✅ Flask app starting...")
    print(f"🔑 HF Token loaded: {'✅ Yes' if token else '❌ NOT FOUND — check your .env file'}")
    app.run(debug=True)