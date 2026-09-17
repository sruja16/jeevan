import os
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# --------------------------------------------------
# 1. Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "training_data.csv"
)

MODEL_DIR = os.path.join(BASE_DIR, "model")

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "course_model.pkl"
)


# --------------------------------------------------
# 2. Load dataset
# --------------------------------------------------

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully")
print("Dataset shape:", df.shape)


# --------------------------------------------------
# 3. Separate features and target
# --------------------------------------------------

X = df.drop(columns=["recommended_course"])

y = df["recommended_course"]


# --------------------------------------------------
# 4. Identify categorical and numerical columns
# --------------------------------------------------

categorical_features = [
    "stream",
    "interest"
]

numerical_features = [
    "maths",
    "physics",
    "chemistry",
    "biology",
    "computer_science",
    "accountancy",
    "economics",
    "english"
]


# --------------------------------------------------
# 5. Preprocessing
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# --------------------------------------------------
# 6. ML model
# --------------------------------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)


# --------------------------------------------------
# 7. Create pipeline
# --------------------------------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", model)
    ]
)


# --------------------------------------------------
# 8. Train-test split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# --------------------------------------------------
# 9. Train
# --------------------------------------------------

print("\nTraining model...")

pipeline.fit(X_train, y_train)


# --------------------------------------------------
# 10. Evaluate
# --------------------------------------------------

y_pred = pipeline.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Evaluation")
print("----------------")
print("Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))


# --------------------------------------------------
# 11. Save model
# --------------------------------------------------

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(
    pipeline,
    MODEL_PATH
)

print("\nModel saved successfully!")
print("Saved to:", MODEL_PATH)