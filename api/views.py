from rest_framework.decorators import api_view
from rest_framework.response import Response
from ai_engine.predictor import predict_symptom_allergy

@api_view(["POST"])
def symptom_prediction(request):
    symptoms = request.data.get("symptoms")

    if not symptoms:
        return Response({"error": "Symptoms are required"})

    result = predict_symptom_allergy(symptoms)
    return Response(result)