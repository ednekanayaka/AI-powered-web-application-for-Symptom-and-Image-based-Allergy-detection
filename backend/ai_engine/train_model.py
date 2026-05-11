import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ==========================================
# Paths
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "symptom_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")

# ==========================================
# STEP 1: Create Symptom Dataset (Binary)
# ==========================================
data = {
    "text": [
        "itchy skin rash swelling",
        "sneezing runny nose itching eyes",
        "skin redness swelling allergy",
        "difficulty breathing wheezing",
        "shortness of breath chest tightness",
        "watery eyes sneezing pollen",
        "food caused stomach pain itching",
        "drug reaction skin rash",
        "headache nausea vomiting",
        "fever cough body pain",
        "stomach pain diarrhea",
        "muscle pain fatigue"
    ],
    # 1 = Allergy, 0 = Not Allergy
    "label": [1,1,1,1,1,1,1,1,0,0,0,0]
}

df = pd.DataFrame(data)

# ==========================================
# STEP 2: Train-Test Split
# ==========================================
X_train, X_test, y_train, y_test = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42
)

# ==========================================
# STEP 3: Vectorization (TF-IDF)
# ==========================================
vectorizer = TfidfVectorizer(stop_words="english")
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# ==========================================
# STEP 4: Train Model (Logistic Regression)
# ==========================================
model = LogisticRegression()
model.fit(X_train_vec, y_train)

# ==========================================
# STEP 5: Evaluate
# ==========================================
y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)

print(f"✅ Model Accuracy: {accuracy:.2f}")

# ==========================================
# STEP 6: Save Model & Vectorizer
# ==========================================
joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("✅ symptom_model.pkl saved")
print("✅ tfidf_vectorizer.pkl saved")
print("🎉 TRAINING COMPLETED SUCCESSFULLY")