from django.urls import path

from authors.apps.authentication.views import (SocialView, UserRetrieveUpdateAPIView,\
                                               RegistrationAPIView, LoginAPIView \
    ,
                                               ForgotPasswordView,
                                               UserActivationAPIView,
                                               ChangePasswordView)

urlpatterns = [
    path('user/profile', UserRetrieveUpdateAPIView.as_view(), name="user-retrieve-profile"),
    path('users/', RegistrationAPIView.as_view(), name="user-signup"),
    path('users/login/', LoginAPIView.as_view(), name="user-login"),
    path('users/forgot_password/', ForgotPasswordView.as_view(), name="forgot_password"),
    path('users/change_password/<str:token>', ChangePasswordView.as_view(), name="change_password"),
    path('auth/<str:token>', UserActivationAPIView.as_view(), name="user-activate"),
    path('social/login/', SocialView.as_view(), name='social_auth'),
]
