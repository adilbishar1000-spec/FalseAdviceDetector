import pandas as pd
import random

# ----------------------------
# Health Categories + Templates
# ----------------------------

diseases = ["diabetes", "thyroid", "blood pressure", "asthma", "cancer"]
remedies = ["warm water", "lemon water", "turmeric", "garlic", "honey"]

safe_templates = [
    "Drink water daily to stay hydrated",
    "Exercise improves overall health",
    "Eating fruits supports immunity",
    "Sleep 7-8 hours for good health",
    "Consult a doctor for medical issues",
    "Vaccines prevent serious infections",
]

misleading_templates = [
    "{remedy} cures {disease} permanently",
    "{remedy} detox removes toxins from the body",
    "Home remedies guarantee complete cure of {disease}",
    "Drinking {remedy} fixes {disease} naturally",
    "{remedy} works better than medicine for {disease}",
]

dangerous_templates = [
    "Stop taking medicine for {disease} and use {remedy}",
    "Replace doctor treatment with {remedy} for {disease}",
    "No need for insulin if you drink {remedy}",
    "Quit antibiotics and follow {remedy} cure",
    "Doctors are unnecessary, treat {disease} at home",
]

# ----------------------------
# Generate Dataset
# ----------------------------

def create_dataset(samples=300):
    data = []

    for _ in range(samples):
        # Safe Advice
        safe = random.choice(safe_templates)
        data.append([safe, 0])

        # Misleading Advice
        mis = random.choice(misleading_templates).format(
            remedy=random.choice(remedies),
            disease=random.choice(diseases)
        )
        data.append([mis, 1])

        # Dangerous Advice
        danger = random.choice(dangerous_templates).format(
            remedy=random.choice(remedies),
            disease=random.choice(diseases)
        )
        data.append([danger, 2])

    random.shuffle(data)

    df = pd.DataFrame(data, columns=["text", "label"])
    df.to_csv("health_advice_dataset.csv", index=False)

    print("✅ Next-Level Dataset Generated!")
    print("Total Rows:", len(df))
    print("Saved as health_advice_dataset.csv")


if __name__ == "__main__":
    create_dataset(samples=400)
