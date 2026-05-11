import os
import numpy as np
import joblib
from tensorflow.keras.models import load_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# =========================================
# ✅ LOAD MODELS
# =========================================
symptom_model = None
image_model = None

try:
    symptom_model = joblib.load(os.path.join(BASE_DIR, "symptom_model.pkl"))
    print("[OK] Symptom model loaded")
except Exception as e:
    print("[ERROR] Symptom model failed:", e)

try:
    image_model = load_model(os.path.join(BASE_DIR, "skin_allergy_model.keras"))
    print("[OK] Image model loaded")
except Exception as e:
    print("[ERROR] Image model failed:", e)


# =========================================
# 🧠 SYMPTOM PREDICTION
# =========================================
def predict_symptom_allergy(symptoms):

    try:
        if not symptoms:
            return "Unknown"

        text = " ".join(symptoms).lower()

        # Try ML model
        if symptom_model is not None:
            try:
                pred = symptom_model.predict([text])
                return str(pred[0])
            except Exception as e:
                print("[WARN] Symptom ML failed:", e)

        # Fallback rules
        if any(x in text for x in ["rash", "itch", "red", "swelling"]):
            return "Skin Allergy"

        elif any(x in text for x in ["sneeze", "cough", "runny nose"]):
            return "Respiratory Allergy"

        elif any(x in text for x in ["vomit", "nausea", "diarrhea", "stomach"]):
            return "Food Allergy"

        return "No Allergy"

    except Exception as e:
        print("[ERROR] Symptom error:", e)
        return "Unknown"


# =========================================
# 🖼 IMAGE PREDICTION (IMPROVED 🚀)
# =========================================
def predict_image_allergy(image_array):

    try:
        if image_model is None:
            return "Model not loaded", 0

        # =========================
        # 🔍 1. BASIC VALIDATION
        # =========================
        if image_array is None or image_array.size == 0:
            return "Invalid Image", 0

        # =========================
        # 📊 2. IMAGE STATS
        # =========================
        mean = np.mean(image_array)
        std = np.std(image_array)

        print(f"stats: mean={mean:.2f}, std={std:.2f}")

        # Reject blank / extreme images
        if std < 8:
            return "Invalid Image (Too Flat)", 5

        if mean > 245 or mean < 10:
            return "Invalid Image (Lighting Issue)", 5

        # =========================
        # 🎨 3. SKIN COLOR DETECTION
        # =========================
        r = image_array[:, :, 0]
        g = image_array[:, :, 1]
        b = image_array[:, :, 2]

        # Skin mask (simple rule)
        skin_mask = (
            (r > 95) & (g > 40) & (b > 20) &
            ((np.max(image_array, axis=2) - np.min(image_array, axis=2)) > 15) &
            (np.abs(r - g) > 15) &
            (r > g) & (r > b)
        )

        skin_ratio = np.sum(skin_mask) / (image_array.shape[0] * image_array.shape[1])

        print(f"skin_ratio={skin_ratio:.4f}")

        # If no skin → reject
        if skin_ratio < 0.05:
            return "No Skin Detected", 10

        # =========================
        # 🧠 4. MODEL PREDICTION
        # =========================
        img = image_array / 255.0
        img = np.expand_dims(img, axis=0)

        pred = float(image_model.predict(img, verbose=0)[0][0])

        print(f"model_output={pred:.4f}")

        confidence = round(pred * 100, 2)

        # =========================
        # 🎯 5. FINAL DECISION
        # =========================
        if pred > 0.85:
            return "Skin Allergy", confidence

        elif pred < 0.35:
            return "No Allergy", round(100 - confidence, 2)

        else:
            return "Uncertain (Upload clearer skin image)", confidence

    except Exception as e:
        print("[ERROR] Image error:", e)
        return "Prediction Failed", 0