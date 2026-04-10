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
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

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
<html>
<head>
    <title>False Health Advice Detector</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
          rel="stylesheet">
    <style>
        body {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e3f2fd 100%);
            font-family: 'Segoe UI', sans-serif;
            min-height: 100vh;
        }}
        .main-card {{
            border-radius: 20px;
            box-shadow: 0px 8px 30px rgba(0,0,0,0.12);
            border: none;
        }}
        .result-card {{
            border-radius: 12px;
            transition: all 0.3s ease;
        }}
        .brand-title {{
            background: linear-gradient(90deg, #1976d2, #42a5f5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }}
        .analyze-btn {{
            background: linear-gradient(90deg, #1976d2, #42a5f5);
            border: none;
            border-radius: 0 8px 8px 0;
        }}
        .analyze-btn:hover {{
            background: linear-gradient(90deg, #1565c0, #1976d2);
        }}
        .form-control {{
            border-radius: 8px 0 0 8px;
        }}
        footer {{
            font-size: 13px;
        }}
    </style>
</head>

<body>
<div class="container mt-5 mb-5">
<div class="card main-card p-4">

    <h2 class="text-center mb-1 brand-title">🩺 False Health Advice Detector</h2>
    <p class="text-center text-muted mb-4" style="font-size:14px;">
        Powered by Machine Learning + Hugging Face AI
    </p>

    <form method="POST" class="mt-2">
        <div class="input-group input-group-lg">
            <input type="text" class="form-control shadow-sm"
                   name="advice"
                   placeholder="e.g. Drinking bleach cures infections..."
                   required>
            <button class="btn btn-primary px-4 analyze-btn">🔍 Analyze</button>
        </div>
    </form>

    <hr class="mt-4">

    {"" if result is None else f"""

    <div class="alert alert-{color} text-center result-card">
        <h3 class="mb-1">{result}</h3>
        <span class="badge bg-secondary fs-6">Confidence: {confidence:.2f}%</span>
    </div>

    <div class="row mt-3 g-3">

        <div class="col-12">
            <div class="card result-card p-3 bg-light border-0 shadow-sm">
                <b>📌 Closest Myth Match:</b><br>
                <i class="text-muted">{matched_text}</i><br>
                <small>Similarity Score: <b>{similarity_score:.2f}</b></small>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card result-card p-3 border-start border-4 border-danger shadow-sm h-100">
                <b>⚠️ Why It&apos;s Risky:</b><br>
                <span class="text-secondary">{reason}</span>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card result-card p-3 border-start border-4 border-success shadow-sm h-100">
                <b>💚 Safe Alternative:</b><br>
                <span class="text-secondary">{safe_tip}</span>
            </div>
        </div>

        <div class="col-12">
            <div class="card result-card p-3 border-start border-4 border-primary shadow-sm">
                <b>🤖 AI Explanation (Hugging Face):</b><br>
                <span class="text-secondary">{chatbot_reply}</span>
            </div>
        </div>

        <div class="col-12">
            <div class="card result-card p-3 border-start border-4 border-warning shadow-sm">
                <b>📘 Offline Explanation:</b><br>
                <span class="text-secondary">{offline_exp}</span>
            </div>
        </div>

    </div>

    """}

    <p class="text-center mt-4 text-muted footer">
        ⚠️ This tool is for educational purposes only. Always consult a licensed doctor for medical advice.
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