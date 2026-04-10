import time
import argparse
...
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import pickle

print("✅ Training started...")

# STEP 1: Load dataset
data = pd.read_csv("health_advice_dataset.csv")

X = data["text"]
y = data["label"]

# STEP 2: Convert Text → TF-IDF Features
vectorizer = TfidfVectorizer(stop_words="english")
X_tfidf = vectorizer.fit_transform(X)

# STEP 3: Split into Train & Test
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.2, random_state=42
)

# STEP 4: Train Naive Bayes Model
model = MultinomialNB()
model.fit(X_train, y_train)

# STEP 5: Prediction on Test Set
y_pred = model.predict(X_test)

# STEP 6: Print Model Report
print("\n📌 Classification Report:\n")
print(classification_report(y_test, y_pred))

# STEP 7: Save Model + Vectorizer
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Training completed successfully!")
print("✅ model.pkl and vectorizer.pkl saved!")
import time
import argparse
...

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import pickle

print("✅ Training started...")

# Load dataset
data = pd.read_csv("health_advice_dataset.csv")

X = data["text"]
y = data["label"]

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(stop_words="english")
X_tfidf = vectorizer.fit_transform(X)

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y, test_size=0.2, random_state=42
)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)

print("\n📌 Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save Model
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("\n✅ Training completed successfully!")
print("✅ model.pkl and vectorizer.pkl saved!")

import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
data = pd.read_csv("health_myth_dataset_500.csv")

# ✅ Load dataset


# ✅ Clean labels
data["label"] = data["label"].astype(str).str.strip()

label_map = {"Safe": 0, "Misleading": 1, "Dangerous": 2}
data["label_num"] = data["label"].map(label_map)

# ✅ Show invalid labels
print("Invalid labels:", data[data["label_num"].isna()]["label"].unique())

# ✅ Drop NaN labels
data = data.dropna(subset=["label_num"])



# ✅ Convert labels to numbers
label_map = {"Safe": 0, "Misleading": 1, "Dangerous": 2}
data["label_num"] = data["label"].map(label_map)

# ✅ Features (X) and Target (y)
X = data["text"]
y = data["label_num"]

# ✅ TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X)

# ✅ Train Model
model = MultinomialNB()
model.fit(X_vec, y)

# ✅ Save Model and Vectorizer
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("✅ Model trained successfully with myth dataset!")


