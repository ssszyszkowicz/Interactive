from django.urls import path
from . import views

urlpatterns = [
    path('save_profile/', views.save_profile, name='save_profile'),
    path('load_profiles/', views.load_profiles, name='load_profiles'),
    path('load_profile/<int:profile_id>/', views.load_profile, name='load_profile'),
]
