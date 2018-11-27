from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name="user-retrieve-profile"),
    path('users/', RegistrationAPIView.as_view(), name="user-signup"),
    path('users/login/', LoginAPIView.as_view(), name="user-login"),
]
