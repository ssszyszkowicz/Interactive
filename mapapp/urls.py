from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path('change_geo/', views.change_geo, name='change_geo'),
]
