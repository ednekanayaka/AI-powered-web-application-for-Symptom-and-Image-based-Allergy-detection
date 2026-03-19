import os
import pickle
import numpy as np
import cv2

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Prediction

# ✅ TensorFlow imports (rename to avoid conflict)
from tensorflow.keras.models import load_model as keras_load_model
from tensorflow.keras.preprocessing import image


# ==========================================
# Load KERAS AI MODEL (your trained model)
# ==========================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

KERAS_MODEL_PATH = os.path.join(BASE_DIR, "skin_allergy_model.keras")

print("Loading Keras model from:", KERAS_MODEL_PATH)

try:
    keras_model = keras_load_model(KERAS_MODEL_PATH)
    print("Keras model loaded successfully")
except Exception as e:
    print("Error loading Keras model:", e)
    keras_model = None


# ==========================================
# Load PKL Models (OLD SYSTEM)
# ==========================================

SYMPTOM_MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
IMAGE_MODEL_PATH = os.path.join(BASE_DIR, "image_model.pkl")


def load_pkl_model(path, name):
    try:
        if os.path.exists(path):
            with open(path, "rb") as f:
                print(f"{name} loaded successfully")
                return pickle.load(f)
        else:
            print(f"{name} NOT FOUND at:", path)
            return None
    except Exception as e:
        print(f"{name} LOAD ERROR:", e)
        return None


symptom_model = load_pkl_model(SYMPTOM_MODEL_PATH, "SYMPTOM MODEL")
image_model = load_pkl_model(IMAGE_MODEL_PATH, "OLD IMAGE MODEL")


# ==========================================
# Helper user function
# ==========================================

def get_default_user():
    return User.objects.first()


# ==========================================
# 🔹 Symptom Prediction API (unchanged)
# ==========================================

@api_view(['POST'])
def predict_allergy(request):

    if symptom_model is None:
        return Response({"error": "Symptom model not found"}, status=500)

    symptoms = request.data.get("symptoms")

    if not symptoms:
        return Response({"error": "Symptoms required"}, status=400)

    try:
        prediction = symptom_model.predict([symptoms])[0]

        Prediction.objects.create(
            user=get_default_user(),
            symptoms=symptoms,
            prediction=str(prediction)
        )

        return Response({"prediction": prediction})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# ==========================================
# 🔥 NEW IMAGE MODEL (KERAS) PREDICTION
# ==========================================

def predict_skin_keras(img_path):

    if keras_model is None:
        return "Model not loaded"

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = keras_model.predict(img_array)

    if prediction < 0.5:
        return "Allergy (Eczema)"
    else:
        return "Not Allergy"


# ==========================================
# 🔹 IMAGE API (UPDATED TO USE KERAS MODEL)
# ==========================================

class PredictImageAllergyView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):

        if 'image' not in request.FILES:
            return Response({"error": "Image required"}, status=400)

        try:
            image_file = request.FILES['image']

            # Save image
            media_dir = "media"
            os.makedirs(media_dir, exist_ok=True)

            file_path = os.path.join(media_dir, image_file.name)

            with open(file_path, "wb+") as f:
                for chunk in image_file.chunks():
                    f.write(chunk)

            # 🔥 Use KERAS MODEL
            result = predict_skin_keras(file_path)

            # Save prediction
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
            return Response({"error": str(e)}, status=500)