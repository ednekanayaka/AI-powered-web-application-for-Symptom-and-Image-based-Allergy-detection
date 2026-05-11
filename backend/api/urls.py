from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('predict/', views.predict_allergy, name='predict_allergy'),
    path('test/', views.test_api, name='test_api'),
    path('diet/', views.diet_plan, name='diet_plan'),
    path('diet-ai/', views.diet_by_symptom, name='diet_by_symptom'),
    path('history/', views.meal_history, name='meal_history'),
    path('dashboard/', views.dashboard_data, name='dashboard_data'),
    path('register/', views.register_user, name='register_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('save-health/', views.save_health_data, name='save_health_data'),
    path('settings/', views.user_settings, name='user_settings'),
    path('exercise/', views.exercise_plan, name='exercise_plan'),
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('admin/users/', views.admin_users_list, name='admin_users_list'),
    path('admin/users/<int:user_id>/', views.admin_user_delete, name='admin_user_delete'),
    path('admin/diet/', views.admin_diet_list, name='admin_diet_list'),
    path('admin/diet/<int:plan_id>/', views.admin_diet_detail, name='admin_diet_detail'),
    path('admin/exercise/', views.admin_exercise_list, name='admin_exercise_list'),
    path('admin/exercise/<int:plan_id>/', views.admin_exercise_detail, name='admin_exercise_detail'),
    path('daily-log/', views.daily_log, name='daily_log'),
]
