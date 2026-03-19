import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SYMPTOM_MODEL_PATH = os.path.join(BASE_DIR, "symptom_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "tfidf_vectorizer.pkl")

# Load using joblib (IMPORTANT)
symptom_model = joblib.load(SYMPTOM_MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("SYMPTOM MODEL loaded successfully")

def predict_symptom_allergy(symptom_text):
    X = vectorizer.transform([symptom_text])
    prob = symptom_model.predict_proba(X)[0][1]

    return {
        "prediction": "Allergy Detected" if prob >= 0.4 else "No Allergy Detected",
        "probability": round(float(prob), 3)
    }