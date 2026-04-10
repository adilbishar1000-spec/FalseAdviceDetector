import pandas as pd
import random

# ----------------------------
# Myth Categories + Templates
# ----------------------------

diseases = ["diabetes", "thyroid", "blood pressure", "asthma", "cancer", "kidney disease"]
remedies = ["turmeric", "garlic", "honey", "lemon water", "herbal tea", "warm water"]

safe_tips = [
    ("Drink water daily", "General hydration advice", "Stay hydrated regularly"),
    ("Exercise improves health", "Encourages fitness habits", "Do moderate exercise daily"),
    ("Eat fruits and vegetables", "Healthy nutrition guidance", "Maintain a balanced diet"),
    ("Sleep 7-8 hours daily", "Promotes good rest", "Follow a proper sleep routine"),
    ("Consult a doctor when sick", "Medical supervision is important", "Seek professional healthcare"),
]

misleading_templates = [
    ("{remedy} cures {disease} permanently",
     "No scientific evidence for permanent cure claims",
     "Consult a medical specialist"),
    ("Drinking {remedy} detox removes all toxins",
     "Detox claims are unverified medically",
     "Maintain healthy lifestyle and hydration"),
    ("Home remedies guarantee cure of {disease}",
     "Guaranteed cure promises are misleading",
     "Follow evidence-based medical care"),
    ("{remedy} works better than medicines for {disease}",
     "Herbal remedies cannot fully replace treatment",
     "Continue doctor-prescribed treatment"),
]

dangerous_templates = [
    ("Stop taking medicine for {disease} and use {remedy}",
     "Stopping prescribed medicine can cause serious harm",
     "Never stop treatment without doctor approval"),
    ("Replace antibiotics with {remedy}",
     "Untreated infections may become severe",
     "Complete the full antibiotic course"),
    ("Quit insulin injections and drink {remedy}",
     "Insulin is life-saving for diabetes patients",
     "Continue insulin under endocrinologist guidance"),
    ("Doctors are unnecessary, treat {disease} at home",
     "Avoiding medical care can lead to complications",
     "Always consult qualified healthcare professionals"),
]

# ----------------------------
# Generate Dataset
# ----------------------------

def generate_dataset(samples=500):
    data = []

    # Safe rows
    for tip, reason, safe_tip in safe_tips:
        data.append([tip, "Safe", reason, safe_tip])

    # Generate misleading + dangerous myths
    while len(data) < samples:
        disease = random.choice(diseases)
        remedy = random.choice(remedies)

        # Misleading
        myth, reason, safe = random.choice(misleading_templates)
        text = myth.format(remedy=remedy, disease=disease)
        data.append([text, "Misleading", reason, safe])

        # Dangerous
        myth, reason, safe = random.choice(dangerous_templates)
        text = myth.format(remedy=remedy, disease=disease)
        data.append([text, "Dangerous", reason, safe])

    # Shuffle dataset
    random.shuffle(data)

    # Create DataFrame
    df = pd.DataFrame(data, columns=["text", "label", "reason", "safe_tip"])

    # Save CSV
    df.to_csv("health_myth_dataset_500.csv", index=False)

    print("✅ 500+ Myth Dataset Generated Successfully!")
    print("Saved File: health_myth_dataset_500.csv")
    print("Total Rows:", len(df))


if __name__ == "__main__":
    generate_dataset(500)
