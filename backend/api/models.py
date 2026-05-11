from django.contrib.auth.models import User
from django.db import models


class MealHistory(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    symptoms = models.TextField()
    meal_items = models.TextField(blank=True, null=True)
    prediction = models.CharField(max_length=255)
    food_allergy = models.BooleanField(default=False)
    trigger_foods = models.TextField(blank=True, null=True)
    confidence = models.IntegerField(default=0)
    risk = models.CharField(max_length=50, default="Low")
    calories = models.IntegerField(blank=True, null=True)
    protein = models.CharField(max_length=50, blank=True, null=True)
    diet = models.TextField(blank=True, null=True)
    avoid = models.TextField(blank=True, null=True)
    exercise = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def get_list(self, field):
        value = getattr(self, field)
        return value.split(",") if value else []


class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=100)
    height = models.FloatField()
    weight = models.FloatField()
    calories = models.IntegerField(null=True, blank=True)
    exercise_minutes = models.IntegerField(null=True, blank=True)
    bmi = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - BMI: {self.bmi}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    fitness_goal = models.CharField(max_length=255, null=True, blank=True)
    allergies = models.CharField(max_length=255, null=True, blank=True)
    is_admin = models.BooleanField(default=False)

    def calculate_bmi(self):
        if self.weight and self.height:
            h = float(self.height)
            h_m = h / 100 if h > 3 else h
            if h_m > 0:
                return round(self.weight / (h_m ** 2), 2)
        return 0

    def __str__(self):
        return self.user.username


class MealPlan(models.Model):
    goal_type = models.CharField(max_length=50)
    meal_type = models.CharField(max_length=50)
    day = models.IntegerField(default=1)
    name = models.CharField(max_length=150)
    calories = models.IntegerField()
    protein = models.CharField(max_length=50)
    image_url = models.URLField(max_length=500, blank=True, null=True)


class ExercisePlan(models.Model):
    goal_type = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    sets = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.goal_type} - {self.name}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message}"
