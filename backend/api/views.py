import json

import numpy as np
from PIL import Image
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from ai_engine.predictor import predict_image_allergy, predict_symptom_allergy
from .image_catalog import get_image_url_for_title
from .models import HealthData, MealHistory, UserProfile


def parse_list(data):
    if not data:
        return []

    if isinstance(data, list):
        return data

    if isinstance(data, str):
        try:
            return json.loads(data)
        except Exception:
            return [x.strip() for x in data.split(",") if x.strip()]

    return []


def resolve_goal_type(goal_text):
    goal = (goal_text or "").strip().lower()
    if "muscle" in goal or "gain" in goal:
        return "muscle"
    if "lose" in goal or "weight" in goal or "cut" in goal:
        return "lose"
    return "general"


MEAL_SLOT_ORDER = ["breakfast", "lunch", "dinner"]


def normalize_meal_type(value):
    return (value or "").strip().lower()


def fallback_image_url(value, query, kind="meal"):
    if value and str(value).strip():
        return value
    return get_image_url_for_title(query, kind=kind)


@api_view(["POST"])
def predict_allergy(request):
    try:
        symptoms = parse_list(request.data.get("symptoms"))
        meal_items = parse_list(request.data.get("meal_items"))
        image = request.FILES.get("image")

        if not symptoms and not image and not meal_items:
            return Response(
                {"error": "Provide symptoms, image, or meal items"},
                status=status.HTTP_400_BAD_REQUEST
            )

        prediction = "Unknown"
        confidence = 0

        if image:
            img = Image.open(image).convert("RGB")
            img = img.resize((224, 224))
            img_array = np.array(img)
            prediction, confidence = predict_image_allergy(img_array)

        if symptoms:
            symptom_pred = predict_symptom_allergy(symptoms)
            if prediction and prediction != "Unknown":
                if symptom_pred.lower() in prediction.lower():
                    confidence += 5
                else:
                    confidence -= 5
            else:
                prediction = symptom_pred
                confidence = 85

        confidence = max(0, min(100, int(confidence)))
        pred_lower = prediction.lower() if prediction else ""

        common_allergens = [
            "milk", "cheese", "butter", "dairy",
            "peanut", "nuts", "egg",
            "seafood", "fish", "shrimp",
            "wheat", "soy"
        ]

        if request.user.is_authenticated:
            try:
                profile = request.user.userprofile
                if profile.allergies:
                    user_allergies = [a.strip().lower() for a in profile.allergies.split(",") if a.strip()]
                    common_allergens.extend(user_allergies)
            except Exception:
                pass

        common_allergens = list(set(common_allergens))
        trigger_foods = [food for food in meal_items if food.lower() in common_allergens]
        food_allergy = False

        if trigger_foods and (not prediction or "unknown" in pred_lower or "skin" in pred_lower or "allergy" in pred_lower):
            food_allergy = True
            prediction = "Food Allergy"
            confidence = max(confidence, 90)

        if "no allergy" in pred_lower:
            risk = "None"
        elif food_allergy:
            risk = "High"
        elif "skin" in pred_lower:
            risk = "Medium"
        else:
            risk = "Low"

        if food_allergy:
            diet = [
                "Avoid: " + ", ".join(trigger_foods),
                "Drink more water",
                "Eat fresh fruits"
            ]
        else:
            diet = ["Balanced diet", "Avoid junk food"]

        exercise = ["Walking", "Yoga", "Breathing"]

        MealHistory.objects.create(
            user=request.user if request.user.is_authenticated else None,
            symptoms=",".join(symptoms) if symptoms else "image_input",
            prediction=prediction,
            calories=1300,
            protein="60g",
            avoid=",".join(diet)
        )

        return Response({
            "status": "success",
            "prediction": prediction,
            "food_allergy": food_allergy,
            "trigger_foods": trigger_foods,
            "risk": risk,
            "confidence": confidence,
            "diet": diet,
            "exercise": exercise
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
def test_api(request):
    return Response({"message": "Backend working"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def meal_history(request):
    data = MealHistory.objects.filter(user=request.user).values()
    return Response(data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def diet_plan(request):
    try:
        profile = request.user.userprofile
        goal = profile.fitness_goal if profile.fitness_goal else ""
        allergies = profile.allergies.lower() if profile.allergies else ""
        avoid = [a.strip() for a in allergies.split(",") if a.strip()]
    except Exception:
        goal = ""
        avoid = []

    target_goal = resolve_goal_type(goal)

    from .models import MealPlan

    meal_records = MealPlan.objects.filter(goal_type=target_goal).order_by("day", "id")

    if not meal_records.exists() and target_goal == "muscle":
        meal_records = MealPlan.objects.filter(goal_type="gain").order_by("day", "id")

    if not meal_records.exists() and target_goal != "general":
        meal_records = MealPlan.objects.filter(goal_type="general").order_by("day", "id")

    day_slot_map = {}

    for meal in meal_records:
        day_num = meal.day
        slot = normalize_meal_type(meal.meal_type)
        if slot not in MEAL_SLOT_ORDER:
            continue

        if day_num not in day_slot_map:
            day_slot_map[day_num] = {}

        if slot in day_slot_map[day_num]:
            existing = day_slot_map[day_num][slot]
            if (not existing.image_url) and meal.image_url:
                day_slot_map[day_num][slot] = meal
            continue

        day_slot_map[day_num][slot] = meal

    result_days = []
    for day in range(1, 8):
        if day in day_slot_map:
            meals = []
            for slot in MEAL_SLOT_ORDER:
                meal = day_slot_map[day].get(slot)
                if not meal:
                    continue

                meal_name_lower = meal.name.lower()
                matched_allergies = []
                for allergen in avoid:
                    if allergen and allergen in meal_name_lower:
                        matched_allergies.append(allergen)

                meals.append({
                    "title": slot.capitalize(),
                    "name": meal.name,
                    "calories": meal.calories,
                    "protein": meal.protein,
                    "image": fallback_image_url(meal.image_url, meal.name, kind="meal"),
                    "day": meal.day,
                    "is_safe": len(matched_allergies) == 0,
                    "matched_allergies": matched_allergies,
                })

            result_days.append({
                "day": day,
                "meals": meals
            })

    return Response({
        "goal": target_goal,
        "days": result_days,
        "avoid": avoid
    })


@api_view(["POST"])
def diet_by_symptom(request):
    symptoms = parse_list(request.data.get("symptoms"))

    if not symptoms:
        return Response({"error": "Symptoms required"}, status=400)

    prediction = predict_symptom_allergy(symptoms)
    return Response({
        "prediction": prediction,
        "avoid": ["Junk food", "Processed food"]
    })


@api_view(["POST"])
def register_user(request):
    try:
        username = request.data.get("username")
        password = request.data.get("password")
        full_name = request.data.get("full_name")
        age = request.data.get("age")
        gender = request.data.get("gender")
        height = request.data.get("height")
        weight = request.data.get("weight")
        fitness_goal = request.data.get("fitness_goal")
        allergies = request.data.get("allergies")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        user = User.objects.create_user(
            username=username,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            age=int(age) if age else None,
            gender=gender,
            height=float(height) if height else None,
            weight=float(weight) if weight else None,
            fitness_goal=fitness_goal,
            allergies=allergies
        )

        return Response({
            "status": "success",
            "message": "User registered successfully"
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["POST"])
def save_health_data(request):
    try:
        height = float(request.data.get("height"))
        weight = float(request.data.get("weight"))
        bmi = round(weight / (height * height), 2)

        HealthData.objects.create(
            user=request.user if request.user.is_authenticated else None,
            user_name=request.user.username if request.user.is_authenticated else "User",
            height=height,
            weight=weight,
            bmi=bmi
        )

        return Response({"bmi": bmi})
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    try:
        user = request.user
        try:
            profile = user.userprofile
            bmi = profile.calculate_bmi()
            username = profile.full_name or user.username
            fitness_goal = profile.fitness_goal
            allergies = profile.allergies
            weight = profile.weight
            height = profile.height
        except Exception:
            bmi = 0
            username = user.username
            fitness_goal = None
            allergies = None
            weight = None
            height = None

        all_history = list(HealthData.objects.filter(user=user).order_by("-created_at")[:30])
        chart_history = list(HealthData.objects.filter(user=user).order_by("created_at")[:7])
        data = chart_history[-1] if chart_history else None

        chart_data = []
        for history_item in chart_history:
            chart_data.append({
                "day": history_item.created_at.strftime("%a %d"),
                "value": history_item.bmi
            })

        if not chart_data:
            chart_data = [{"day": "Today", "value": bmi}]

        log_history = [
            {
                "date": history_item.created_at.strftime("%d %b %Y"),
                "time": history_item.created_at.strftime("%I:%M %p"),
                "weight": history_item.weight,
                "bmi": history_item.bmi,
                "exercise_minutes": history_item.exercise_minutes,
                "calories": history_item.calories,
            }
            for history_item in all_history
        ]

        return Response({
            "username": username,
            "bmi": data.bmi if data else bmi,
            "calories": getattr(data, "calories", None) or 1800,
            "exercise": getattr(data, "exercise_minutes", None),
            "chart_data": chart_data,
            "log_history": log_history,
            "fitness_goal": fitness_goal,
            "allergies": allergies,
            "weight": weight,
            "height": height
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def user_settings(request):
    try:
        profile = request.user.userprofile
    except Exception:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == "POST":
        profile.full_name = request.data.get("full_name", profile.full_name)
        profile.age = request.data.get("age", profile.age)
        profile.gender = request.data.get("gender", profile.gender)
        profile.height = request.data.get("height", profile.height)
        profile.weight = request.data.get("weight", profile.weight)
        profile.fitness_goal = request.data.get("fitness_goal", profile.fitness_goal)
        profile.allergies = request.data.get("allergies", profile.allergies)
        profile.save()

        if profile.height and profile.weight:
            h = float(profile.height)
            h_m = h / 100 if h > 3 else h
            w = float(profile.weight)
            if h_m > 0:
                bmi = round(w / (h_m * h_m), 2)
                HealthData.objects.create(
                    user=request.user,
                    user_name=profile.full_name or request.user.username,
                    height=h,
                    weight=w,
                    bmi=bmi
                )

        return Response({"status": "success", "message": "Settings updated"})

    return Response({
        "full_name": profile.full_name,
        "age": profile.age,
        "gender": profile.gender,
        "height": profile.height,
        "weight": profile.weight,
        "fitness_goal": profile.fitness_goal,
        "allergies": profile.allergies
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def exercise_plan(request):
    try:
        profile = request.user.userprofile
        goal = profile.fitness_goal if profile.fitness_goal else ""
    except Exception:
        goal = ""

    target_goal = resolve_goal_type(goal)

    from .models import ExercisePlan

    exercise_records = ExercisePlan.objects.filter(goal_type=target_goal).order_by("id")
    if not exercise_records.exists() and target_goal == "muscle":
        exercise_records = ExercisePlan.objects.filter(goal_type="gain").order_by("id")
    if not exercise_records.exists() and target_goal != "general":
        exercise_records = ExercisePlan.objects.filter(goal_type="general").order_by("id")

    exercises = []
    for exercise in exercise_records:
        exercises.append({
            "name": exercise.name,
            "sets": exercise.sets,
            "image": fallback_image_url(exercise.image_url, exercise.name, kind="exercise")
        })

    return Response({"exercises": exercises})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    user = request.user
    today = timezone.now().date()

    from .models import Notification

    has_daily = Notification.objects.filter(user=user, created_at__date=today).exists()

    if not has_daily:
        goal = ""
        try:
            goal = user.userprofile.fitness_goal.lower() if user.userprofile.fitness_goal else ""
        except Exception:
            pass

        reminder_msg = "Don't forget to drink 2 liters of water today!"
        if "muscle" in goal or "gain" in goal:
            reminder_msg = "Daily reminder: hit your protein goals for today's muscle recovery."
        elif "lose" in goal or "weight" in goal:
            reminder_msg = "Daily check-in: keep up with your cardio routine."

        Notification.objects.create(user=user, message=reminder_msg)

    notifications = Notification.objects.filter(user=user).order_by("-created_at")[:10]
    return Response([
        {
            "id": notification.id,
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at": notification.created_at.strftime("%Y-%m-%d %H:%M")
        }
        for notification in notifications
    ])


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            profile = user.userprofile
            token['is_admin'] = profile.is_admin
        except Exception:
            token['is_admin'] = False
        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def _is_admin(request):
    if not request.user.is_authenticated:
        return False
    try:
        return request.user.userprofile.is_admin
    except Exception:
        return False


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def admin_users_list(request):
    if not _is_admin(request):
        return Response({"error": "Admin access required"}, status=403)

    users = User.objects.select_related("userprofile").all().order_by("id")
    result = []
    for user in users:
        try:
            profile = user.userprofile
            is_admin = profile.is_admin
            full_name = profile.full_name
            allergies = profile.allergies
            fitness_goal = profile.fitness_goal
        except Exception:
            is_admin = False
            full_name = None
            allergies = None
            fitness_goal = None

        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": full_name,
            "allergies": allergies,
            "fitness_goal": fitness_goal,
            "is_admin": is_admin,
            "date_joined": user.date_joined.strftime("%Y-%m-%d"),
        })

    return Response(result)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def admin_user_delete(request, user_id):
    if not _is_admin(request):
        return Response({"error": "Admin access required"}, status=403)

    try:
        user = User.objects.get(id=user_id)
        if user == request.user:
            return Response({"error": "Cannot delete yourself"}, status=400)
        user.delete()
        return Response({"status": "deleted"})
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def admin_diet_list(request):
    if not _is_admin(request):
        return Response({"error": "Admin access required"}, status=403)

    from .models import MealPlan

    if request.method == "GET":
        plans = MealPlan.objects.all().order_by("goal_type", "day", "meal_type")
        return Response([{
            "id": plan.id,
            "goal_type": plan.goal_type,
            "meal_type": plan.meal_type,
            "day": plan.day,
            "name": plan.name,
            "calories": plan.calories,
            "protein": plan.protein,
            "image_url": plan.image_url,
        } for plan in plans])

    data = request.data
    meal_name = data.get("name", "")
    plan = MealPlan.objects.create(
        goal_type=data.get("goal_type", "general"),
        meal_type=data.get("meal_type", "Breakfast"),
        day=int(data.get("day", 1)),
        name=meal_name,
        calories=int(data.get("calories", 0)),
        protein=data.get("protein", "0g"),
        image_url=fallback_image_url(data.get("image_url", ""), meal_name, kind="meal"),
    )
    return Response({"id": plan.id, "status": "created"}, status=201)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def admin_diet_detail(request, plan_id):
    if not _is_admin(request):
        return Response({"error": "Admin access required"}, status=403)

    from .models import MealPlan

    try:
        plan = MealPlan.objects.get(id=plan_id)
    except MealPlan.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == "DELETE":
        plan.delete()
        return Response({"status": "deleted"})

    data = request.data
    plan.goal_type = data.get("goal_type", plan.goal_type)
    plan.meal_type = data.get("meal_type", plan.meal_type)
    plan.day = int(data.get("day", plan.day))
    plan.name = data.get("name", plan.name)
    plan.calories = int(data.get("calories", plan.calories))
    plan.protein = data.get("protein", plan.protein)
    requested_image = data.get("image_url", plan.image_url)
    plan.image_url = fallback_image_url(requested_image, plan.name, kind="meal")
    plan.save()
    return Response({"status": "updated"})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def admin_exercise_list(request):
    if not _is_admin(request):
        return Response({"error": "Admin access required"}, status=403)

    from .models import ExercisePlan

    if request.method == "GET":
        plans = ExercisePlan.objects.all().order_by("goal_type", "name")
        return Response([{
            "id": plan.id,
            "goal_type": plan.goal_type,
            "name": plan.name,
            "sets": plan.sets,
            "image_url": plan.image_url,
        } for plan in plans])

    data = request.data
    exercise_name = data.get("name", "")
    plan = ExercisePlan.objects.create(
        goal_type=data.get("goal_type", "general"),
        name=exercise_name,
        sets=data.get("sets", ""),
        image_url=fallback_image_url(data.get("image_url", ""), exercise_name, kind="exercise"),
    )
    return Response({"id": plan.id, "status": "created"}, status=201)


@api_view(["PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def admin_exercise_detail(request, plan_id):
    if not _is_admin(request):
        return Response({"error": "Admin access required"}, status=403)

    from .models import ExercisePlan

    try:
        plan = ExercisePlan.objects.get(id=plan_id)
    except ExercisePlan.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == "DELETE":
        plan.delete()
        return Response({"status": "deleted"})

    data = request.data
    plan.goal_type = data.get("goal_type", plan.goal_type)
    plan.name = data.get("name", plan.name)
    plan.sets = data.get("sets", plan.sets)
    requested_image = data.get("image_url", plan.image_url)
    plan.image_url = fallback_image_url(requested_image, plan.name, kind="exercise")
    plan.save()
    return Response({"status": "updated"})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def daily_log(request):
    try:
        weight = request.data.get("weight")
        exercise_minutes = request.data.get("exercise_minutes")
        calories = request.data.get("calories")

        if not weight:
            return Response({"error": "Weight is required to calculate BMI."}, status=400)

        weight = float(weight)
        exercise_minutes = int(exercise_minutes) if exercise_minutes else None
        calories = int(calories) if calories else None

        try:
            profile = request.user.userprofile
            height = float(profile.height) if profile.height else None
            name = profile.full_name or request.user.username
        except Exception:
            height = None
            name = request.user.username

        if not height or height <= 0:
            return Response({"error": "Height not set in your profile. Please update your settings first."}, status=400)

        h_m = height / 100 if height > 3 else height
        bmi = round(weight / (h_m ** 2), 2)

        entry = HealthData.objects.create(
            user=request.user,
            user_name=name,
            height=height,
            weight=weight,
            calories=calories,
            exercise_minutes=exercise_minutes,
            bmi=bmi
        )

        return Response({
            "status": "success",
            "bmi": bmi,
            "weight": weight,
            "exercise_minutes": exercise_minutes,
            "calories": calories,
            "logged_at": entry.created_at.strftime("%Y-%m-%d %H:%M"),
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)
