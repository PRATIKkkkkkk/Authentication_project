from django.urls import path
from .views import StudentAPI, StudentDetailAPI

urlpatterns = [
    path('student/', StudentAPI.as_view()),
    path('student/<int:pk>/', StudentDetailAPI.as_view()),
]