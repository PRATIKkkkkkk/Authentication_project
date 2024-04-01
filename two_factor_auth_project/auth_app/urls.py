from django.urls import path
from .views import UserAPI, Veriy_Email

urlpatterns = [
    path('register/', UserAPI.as_view(), name='register'),
    path('verify_email/', Veriy_Email.as_view(), name='verify_email'),
]