from django.urls import path

from .views import (
    LoginAPIView, RegistrationAPIView, UserRetrieveUpdateAPIView, ForgotPasswordView,
    ChangePasswordView, UserActivationAPIView
)

urlpatterns = [

    path('user/', UserRetrieveUpdateAPIView.as_view(), name="user-retrieve-profile"),
    path('users/', RegistrationAPIView.as_view(), name="user-signup"),
    path('users/login/', LoginAPIView.as_view(), name="user-login"),
    path('users/forgot_password/', ForgotPasswordView.as_view(), name="forgot_password"),
    path('users/change_password/<str:token>', ChangePasswordView.as_view(), name="change_password"),
    path('auth/<str:token>', UserActivationAPIView.as_view(), name="user-activate"),

]
