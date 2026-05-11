import os
import pickle
import numpy as np

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.models import User
from django.conf import settings

from .models import Prediction

# TensorFlow
from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image


# ==========================================
# PATH SETUP
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KERAS_MODEL_PATH = os.path.join(BASE_DIR, "skin_allergy_model.keras")
SYMPTOM_MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")


# ==========================================
# LOAD KERAS MODEL
# ==========================================

print("Loading Keras model from:", KERAS_MODEL_PATH)

try:
    keras_model = keras_load_model(KERAS_MODEL_PATH)
    print("[OK] Keras model loaded successfully")
except Exception as e:
    print("[ERROR] Error loading Keras model:", e)
    keras_model = None


# ==========================================
# LOAD SYMPTOM MODEL
# ==========================================

def load_pkl_model(path):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                print("[OK] Symptom model loaded")
                return pickle.load(f)
        else:
            print("[ERROR] Symptom model NOT FOUND")
            return None
    except Exception as e:
        print("[ERROR] Symptom model error:", e)
        return None


symptom_model = load_pkl_model(SYMPTOM_MODEL_PATH)


# ==========================================
# DEFAULT USER
# ==========================================

def get_default_user():
    return User.objects.first()


# ==========================================
# 🔹 SYMPTOM PREDICTION API (FIXED)
# ==========================================

@api_view(['POST'])
def predict_allergy(request):

    if symptom_model is None:
        return Response({"error": "Symptom model not found"}, status=500)

    try:
        data = request.data
        print("Incoming data:", data)  # DEBUG

        symptoms = data.get("symptoms")

        if not symptoms:
            return Response({"error": "Symptoms required"}, status=400)

        # ✅ HANDLE LIST OR STRING SAFELY
        if isinstance(symptoms, list):
            symptoms_text = " ".join([str(s) for s in symptoms])
        else:
            symptoms_text = str(symptoms)

        symptoms_text = symptoms_text.lower().strip()

        prediction = symptom_model.predict([symptoms_text])[0]

        Prediction.objects.create(
            user=get_default_user(),
            symptoms=symptoms_text,
            prediction=str(prediction)
        )

        return Response({
            "prediction": prediction,
            "message": "Prediction successful"
        })

    except Exception as e:
        return Response({
            "error": "Prediction failed",
            "details": str(e)
        }, status=500)


# ==========================================
# 🔥 IMAGE PREDICTION (KERAS)
# ==========================================

def predict_skin_keras(img_path):

    if keras_model is None:
        return "Model not loaded"

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = keras_model.predict(img_array)[0][0]

    if prediction < 0.5:
        return "Allergy (Eczema)"
    else:
        return "Not Allergy"


# ==========================================
# 🔹 IMAGE API
# ==========================================

class PredictImageAllergyView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):

        if 'image' not in request.FILES:
            return Response({"error": "Image required"}, status=400)

        try:
            image_file = request.FILES['image']

            # ✅ Save inside MEDIA folder properly
            media_root = os.path.join(settings.BASE_DIR, "media")
            os.makedirs(media_root, exist_ok=True)

            file_path = os.path.join(media_root, image_file.name)

            with open(file_path, "wb+") as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            # Predict
            result = predict_skin_keras(file_path)

            # Save result
            Prediction.objects.create(
                user=get_default_user(),
                symptoms="Image Upload",
                prediction=result
            )

            return Response({
                "prediction": result,
                "message": "Prediction successful"
            })

        except Exception as e:
            return Response({
                "error": "Prediction failed",
                "details": str(e)
            }, status=500)