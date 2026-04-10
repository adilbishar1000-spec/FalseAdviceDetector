import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ✅ Load dataset (500 myths)
dataset = pd.read_csv("health_myth_dataset_500.csv")

# Vectorizer for similarity search
sim_vectorizer = TfidfVectorizer()
dataset_vectors = sim_vectorizer.fit_transform(dataset["text"])


def find_best_match(user_input):
    """
    Finds the most similar myth in dataset
    and returns reason + safe tip
    """

    user_vec = sim_vectorizer.transform([user_input])

    similarity_scores = cosine_similarity(user_vec, dataset_vectors)

    best_index = similarity_scores.argmax()
    best_score = similarity_scores[0][best_index]

    best_row = dataset.iloc[best_index]

    return {
        "matched_text": best_row["text"],
        "reason": best_row["reason"],
        "safe_tip": best_row["safe_tip"],
        "score": best_score
    }
