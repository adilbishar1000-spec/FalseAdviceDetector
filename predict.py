import pickle

# Load saved model and vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

def predict_advice(text):
    vec = vectorizer.transform([text])
    prediction = model.predict(vec)[0]

    if prediction == 0:
        return "✅ Safe Advice"
    elif prediction == 1:
        return "⚠️ Misleading Advice"
    else:
        return "🚨 Dangerous Advice"

# ---- USER INPUT ----
user_input = input("Enter health advice: ")

result = predict_advice(user_input)
print("\nResult:", result)
import pickle

# Load trained model & vectorizer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Keywords for explanation
danger_keywords = ["stop", "replace", "no doctor", "quit medicine"]
misleading_keywords = ["cure", "detox", "guaranteed", "permanent"]

def predict_advice(text):
    vec = vectorizer.transform([text])

    prediction = model.predict(vec)[0]
    confidence = max(model.predict_proba(vec)[0]) * 100

    if prediction == 0:
        label = "✅ Safe Advice"
        reason = "General healthy recommendation."
    elif prediction == 1:
        label = "⚠️ Misleading Advice"
        reason = "Unproven cure/detox claim."
    else:
        label = "🚨 Dangerous Advice"
        reason = "Suggests stopping/replacing medical treatment."

    return label, reason, confidence


user_input = input("Enter health advice: ")

label, reason, confidence = predict_advice(user_input)

print("\n--- Result ---")
print("Prediction:", label)
print("Reason:", reason)
print("Confidence:", round(confidence, 2), "%")
