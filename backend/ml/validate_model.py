import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# ==================================================
# LOAD MODEL + VECTORIZER
# ==================================================

model = joblib.load(
    "ml/transaction_model.pkl"
)

vectorizer = joblib.load(
    "ml/vectorizer.pkl"
)


# ==================================================
# LOAD REAL-WORLD VALIDATION DATA
# ==================================================

test_df = pd.read_csv(
    "ml/data/real_world_test.csv"
)

print(
    "Columns:",
    test_df.columns.tolist()
)

print(
    "Validation rows:",
    len(test_df)
)


# ==================================================
# PREPARE DATA
# ==================================================

X_test = (
    test_df["Transaction_Text"]
    .astype(str)
)

y_test = (
    test_df["Label"]
    .astype(str)
    .str.strip()
)


# ==================================================
# VECTORIZE
# ==================================================

X_vectorized = vectorizer.transform(
    X_test
)


# ==================================================
# PREDICT
# ==================================================

predictions = model.predict(
    X_vectorized
)

probabilities = model.predict_proba(
    X_vectorized
)


# ==================================================
# ACCURACY
# ==================================================

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\nREAL-WORLD ACCURACY:")

print(
    round(
        accuracy * 100,
        2
    ),
    "%"
)


# ==================================================
# CLASSIFICATION REPORT
# ==================================================

print(
    "\nCLASSIFICATION REPORT:"
)

print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# ==================================================
# WRONG PREDICTIONS
# ==================================================

print(
    "\nWRONG PREDICTIONS:"
)

wrong_count = 0

for text, actual, predicted, probs in zip(
    X_test,
    y_test,
    predictions,
    probabilities
):

    confidence = max(probs) * 100

    if actual != predicted:

        wrong_count += 1

        print(
            "\nTransaction:",
            text
        )

        print(
            "Actual:",
            actual
        )

        print(
            "Predicted:",
            predicted
        )

        print(
            f"Confidence: {confidence:.1f}%"
        )


print(
    "\nTotal wrong predictions:",
    wrong_count
)


# ==================================================
# LOW CONFIDENCE PREDICTIONS
# ==================================================

print(
    "\nLOW CONFIDENCE PREDICTIONS (< 70%):"
)

low_confidence_count = 0

for text, predicted, probs in zip(
    X_test,
    predictions,
    probabilities
):

    confidence = max(probs) * 100

    if confidence < 70:

        low_confidence_count += 1

        print(
            "\nTransaction:",
            text
        )

        print(
            "Predicted:",
            predicted
        )

        print(
            f"Confidence: {confidence:.1f}%"
        )


print(
    "\nTotal low-confidence predictions:",
    low_confidence_count
)