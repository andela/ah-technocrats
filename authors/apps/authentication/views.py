import datetime
import jwt
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import user_logged_in
from requests.exceptions import HTTPError
from social_django.utils import load_strategy, load_backend
from social_core.exceptions import MissingBackend
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from .models import User
from authors.apps.profiles.models import Profile
from authors.apps.profiles.serializers import ProfileSerializer
from .models import User
from .renderers import UserJSONRenderer
from .serializers import (
    LoginSerializer, RegistrationSerializer, UserSerializer, ResetPasswordRequestSerializer, SocialSerializer
)
from .permissions import IsPostOrIsAuthenticated



class RegistrationAPIView(APIView):
    """ Class for handling user registration. """
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (IsPostOrIsAuthenticated,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer
    
    def get(self, request):
        profiles = Profile.objects.all()
        serializer= ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ Signup a new user. """
        user = request.data.get('user', {})
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Set-up mail for verification
        # An email will be sent to the user so that they can confirm 
        # The link in the email contains the token that will be decoded
        if request.is_secure():
            protocol = "https://"
        else:
            protocol = "http://"
        modeled_user = User(
            username=serializer.data.get("username", ''),
            email=serializer.data.get("email", ''),
        )
        # Get the actual token from the model
        token = modeled_user.jwt_token
        path = reverse('authentication:user-activate', kwargs={'token': token})
        url = protocol + request.get_host() + path
        subject = 'Thank you for signing up!'
        message = """ 
                Welcome. We are glad that you are a part of us. Just one more step and we are good to go.
                Follow the link below to activate your account.
                {} 
                """.format(url)
        from_email = settings.EMAIL_HOST_USER
        to_list = [serializer.data['email']]
        User.send_mail(subject, message, from_email, to_list)
        part1 = "Thank you for signing up with Authors Haven. "
        part2 = "Please head over to your email to verify your account."
        message = part1 + part2
        # Add token and message to the response so we
        # get a JSON object with the token as a return value
        # to the view
        message2 = {'message': message, 'data': serializer.data, "token": token}
        return Response(message2, status=status.HTTP_201_CREATED)


class UserActivationAPIView(APIView):
    """ Activates a user after mail verification. """
    permission_classes = (AllowAny,)

    def get(self, request, token):
        """ Method for getting user token and activating them. """
        # After a successful registration, a user is activated through here
        # The token that was created and sent is decoded to get the user
        # The user's is_active attribute is then set to true
        user = User.decode_jwt(token=token)
        is_registered = User.objects.get(username=user['username'])
        is_registered.is_active = True
        is_registered.save()
        # send confirmation mail
        if request.is_secure():
            protocol = "https://"
        else:
            protocol = "http://"
        path = reverse('authentication:user-login')
        url = protocol + request.get_host() + path
        subject = 'Confirmed!!'
        message = """ Welcome to Authors Haven. Stay tuned for amazing reads.\n
        Follow the link bellow to login. \n   {}""".format(url)
        from_email = settings.EMAIL_HOST_USER
        to_list = [user['email']]
        User.send_mail(subject, message, from_email, to_list)
        message = "Your account has been confirmed. Proceed to login."
        return Response(message, status=status.HTTP_200_OK)


class LoginAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email = user['email'])
        user = user[0]
        user_logged_in.send(sender=type(user), request=request,user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        # There is nothing to validate or save here. Instead, we just want the
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user_data = request.data.get('user', {})
        serializer_data = {
            'username': user_data.get('username', request.user.username),
            'email': user_data.get('email', request.user.email),

            'profile': {
                'avatar': user_data.get('avatar', request.user.profile.avatar),
                'bio': user_data.get('bio', request.user.profile.bio),
                'country': user_data.get('country', request.user.profile.country),
                'website': user_data.get('website', request.user.profile.website),
                'phone': user_data.get('phone', request.user.profile.phone),
            }
        }

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        updated_fields = dict()
        for k,v in user_data.items():
            if k in serializer_data['profile']:
                updated_fields.update({k:v})

        response = {
            "message":"Update successful",
            "updated-fields":updated_fields,
            "new-record":serializer_data
        }

        return Response(response, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    # This view handles sending the password reset request email.
    # We expect the user to enter an email that exists in the database
    # If no user is found a DoesNotExist exception is thrown
    # We generate a token for the link because the one generated by the
    # user models expires quickly. This one expires after 24 hrs
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)

    def post(self, request):
        try:
            requester_data = request.data.get('email')
            user = User.objects.get(email=requester_data)
            token = jwt.encode({
                "email": user.email,
                "iat": datetime.datetime.now(),
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, settings.SECRET_KEY, algorithm='HS256').decode()

            if request.is_secure():
                protocol = "https://"
            else:
                protocol = "http://"
            host = request.get_host()
            path = reverse("authentication:change_password", kwargs={'token': token})
            url = protocol + host + path
            message = """
                        Click on the link to reset your password.
                        {}                    
                        """.format(url)
            send_mail(
                "Password Resetting Link",
                message,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=True
            )
            success_message = {"success": "An email has been sent to your inbox with a password reset link."}
            return Response(success_message, status=status.HTTP_200_OK)
        except (KeyError, User.DoesNotExist):
            error_message = {
                "error": "That email does not exist."
            }
            return Response(error_message, status=status.HTTP_404_NOT_FOUND)


class ChangePasswordView(APIView):
    # This is the view that changes the password.
    # We use a put method. The link that is generated by the Forgot Password view has
    # a token that is decoded here.
    # We use the serializer to check if the password meets the requirements.
    # We then call the set_password method to create the password and then save.
    permission_classes = (AllowAny,)
    serializer_class = ResetPasswordRequestSerializer

    def put(self, request, token, *args, **kwargs):
        try:
            new_password = request.data.get('password')
            serializer = self.serializer_class(data={"password": new_password})
            serializer.is_valid(raise_exception=True)
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            email = decode_token.get('email')
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({"Success": "Your password has been reset"}, status=status.HTTP_201_CREATED)

        except jwt.PyJWTError:
            return Response({"Error": "Invalid token. Please request a new password reset link."}, status=403)
class SocialView(CreateAPIView):
    """Login through social sites (Google, Twitter, Facebook)"""
    permission_classes = (AllowAny,)
    serializer_class = SocialSerializer
    renderer_classes = (UserJSONRenderer,)

    def create(self, request):
        """Takes in the provider token and creates a new user if the user does not exist also retrieves the username and uses it to get the token"""
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get("provider")
        authentic_user = request.user if not request.user.is_anonymous else None
        # Django code to plug into Python Social Auth's functionality
        strategy = load_strategy(request)
        try:
            # Get backend corresponding to provider.
            backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)
            if isinstance(backend, BaseOAuth1):
                # Get access_token and access token secret for Oauth1 used by Twitter
                if "access_token_secret" in request.data:
                    access_token = {
                        'oauth_token': request.data['access_token'],
                        'oauth_token_secret': request.data['access_token_secret']
                    }
                else:
                    return Response(
                        {"error": "Access token secret is required"}, status=status.HTTP_400_BAD_REQUEST
                    )

            elif isinstance(backend, BaseOAuth2):
                # Get access token for OAuth2
                access_token = serializer.data.get("access_token")

        except MissingBackend:
            return Response({"error": "The Provider is invalid"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = backend.do_auth(access_token, user=authentic_user)
        except BaseException as error:
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            user.is_active = True
            # Serialize the user.
            user.save()
        serializer = UserSerializer(user)
        user_data = serializer.data
        modeled_user = User(user_data["username"], user_data["email"])
        user_data["token"] = modeled_user.jwt_token
        return Response(user_data, status=status.HTTP_200_OK)

