"""
Movie Genre Classification

Author: Nysa
Internship: CODSOFT AI Internship

Description:
Train a machine learning model to predict movie genres
from plot summaries using NLP and TF-IDF.
"""

import pandas as pd
import re
import joblib

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC

from sklearn.metrics import accuracy_score


# ---------------- LOAD DATASET ----------------

print("Loading dataset...")

data = pd.read_csv(
    "dataset/train_data.txt",
    sep=" ::: ",
    engine="python",
    names=["id", "title", "genre", "plot"]
)

data.dropna(inplace=True)

print(f"Total movies: {len(data)}")
print(f"Total genres: {data['genre'].nunique()}")


# ---------------- CLEAN TEXT ----------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z\s]", "", text)

    return text


data["plot"] = data["plot"].apply(clean_text)


# ---------------- FEATURES & LABELS ----------------

X = data["plot"]

y = data["genre"]


# ---------------- TRAIN TEST SPLIT ----------------

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42,

    stratify=y

)


# ---------------- TF-IDF ----------------

tfidf = TfidfVectorizer(

    max_features=30000,

    stop_words="english",

    ngram_range=(1,2),

    min_df=2,

    max_df=0.85,

    sublinear_tf=True

)

X_train_tfidf = tfidf.fit_transform(X_train)

X_test_tfidf = tfidf.transform(X_test)


# ---------------- MODEL COMPARISON ----------------

models = {

    "Naive Bayes": MultinomialNB(),

    "Logistic Regression": LogisticRegression(max_iter=1000),

    "Linear SVM": LinearSVC(

    C=2,

    class_weight="balanced",

    random_state=42

)

}

results = {}

best_model = None

best_accuracy = 0


for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(

        X_train_tfidf,

        y_train

    )

    y_pred = model.predict(

        X_test_tfidf

    )

    accuracy = accuracy_score(

        y_test,

        y_pred

    )

    results[name] = accuracy

    print(

        f"{name}: {accuracy*100:.2f}%"

    )

    if accuracy > best_accuracy:

        best_accuracy = accuracy

        best_model = model


# ---------------- BEST MODEL ----------------

best_model_name = max(

    results,

    key=results.get

)

print(

    f"\nBest Model: {best_model_name}"

)


# ---------------- SAVE MODEL ----------------

joblib.dump(

    best_model,

    "saved_model/model.pkl"

)

joblib.dump(

    tfidf,

    "saved_model/tfidf.pkl"

)

print("\nModel saved successfully.")
