from rest_framework import serializers
from .models import Symptom, Allergy, AllergyRecord

# ----------------------
# Symptom Serializer
# ----------------------
class SymptomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptom
        fields = '__all__'

# ----------------------
# Allergy Serializer
# ----------------------
class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'

# ----------------------
# AllergyRecord Serializer (with writable nested fields)
# ----------------------
class AllergyRecordSerializer(serializers.ModelSerializer):
    # For POST/PUT: use IDs to assign allergy & symptoms
    allergy_id = serializers.PrimaryKeyRelatedField(
        queryset=Allergy.objects.all(), source='allergy', write_only=True
    )
    symptoms_ids = serializers.PrimaryKeyRelatedField(
        queryset=Symptom.objects.all(), many=True, source='symptoms', write_only=True
    )

    # For GET: nested representation
    allergy = AllergySerializer(read_only=True)
    symptoms = SymptomSerializer(many=True, read_only=True)

    class Meta:
        model = AllergyRecord
        fields = [
            'id',
            'patient_name',
            'allergy',
            'allergy_id',
            'symptoms',
            'symptoms_ids',
            'detected_date'
        ]
