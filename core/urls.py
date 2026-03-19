from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

    # Home page
    path('', home, name='home'),

    # Users app
    path('users/', include('users.urls')),

    # Allergy detection app (symptoms, image prediction, records)
    path('allergy/', include('allergy_app.urls')),

    # Diet recommendation app
    path('diet/', include('diet.urls')),

    # Exercise recommendation app
    path('exercise/', include('exercise.urls')),

    # AI engine routes
    path('ai/', include('ai_engine.urls')),

    # NEW: API routes
    path('api/', include('api.urls')),
]