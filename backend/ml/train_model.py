import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ==================================================
# LOAD FINAL DATASET
# ==================================================

data_path = "ml/data/final_transactions.csv"

df = pd.read_csv(data_path)

print("Columns:", df.columns.tolist())
print("Total rows:", len(df))

print("\nCategories:")
print(df["Label"].value_counts())


# ==================================================
# PREPARE DATA
# ==================================================

X = df["Transaction_Text"].astype(str)
y = df["Label"].astype(str)


# ==================================================
# TRAIN / TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ==================================================
# TF-IDF
# ==================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2),
    max_features=30000,
    sublinear_tf=True
)

X_train_vectorized = vectorizer.fit_transform(X_train)

X_test_vectorized = vectorizer.transform(X_test)


# ==================================================
# TRAIN MODEL
# ==================================================

model = LogisticRegression(
    max_iter=3000,
    class_weight="balanced"
)

model.fit(
    X_train_vectorized,
    y_train
)


# ==================================================
# EVALUATE
# ==================================================

predictions = model.predict(
    X_test_vectorized
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nModel Accuracy:")
print(round(accuracy * 100, 2), "%")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions
    )
)


# ==================================================
# SAVE MODEL
# ==================================================

joblib.dump(
    model,
    "ml/transaction_model.pkl"
)

joblib.dump(
    vectorizer,
    "ml/vectorizer.pkl"
)

print("\nModel saved successfully.")


# ==================================================
# REAL-WORLD SAMPLE TEST
# ==================================================

sample_transactions = [
    "UPI SWIGGY ORDER 829381",
    "POS AMAZON SELLER SERVICES",
    "INDIAN OIL PETROL PUMP",
    "UPI ZOMATO ONLINE PAYMENT",
    "NETFLIX MONTHLY PAYMENT",
    "COLLEGE FEE PAYMENT",
    "HOUSE RENT AUGUST",
    "APOLLO PHARMACY",
    "AIRTEL RECHARGE",
    "IRCTC ONLINE TICKET",
    "DMART SUPERMARKET PURCHASE",
    "UPI TRANSFER TO FRIEND",
    "SALARY CREDIT AUGUST",
    "PERSONAL LOAN EMI PAYMENT",
    "ZERODHA INVESTMENT PAYMENT"
]

sample_vectors = vectorizer.transform(
    sample_transactions
)

sample_predictions = model.predict(
    sample_vectors
)

sample_probabilities = model.predict_proba(
    sample_vectors
)

print("\nReal-world sample predictions:")

for text, prediction, probabilities in zip(
    sample_transactions,
    sample_predictions,
    sample_probabilities
):

    confidence = max(probabilities) * 100

    print(
        text,
        "=>",
        prediction,
        f"({confidence:.1f}% confidence)"
    )