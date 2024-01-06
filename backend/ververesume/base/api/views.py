import os
import jwt
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (LoginUserSerializer, SignUserSerializer,
                          TokenSerializer, UserForgotPassword, ResetPasswordSerializer)
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db.models import Q
from .utils import create_access_refresh_jwt_token
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import timedelta
from .utils import create_jwt_token
from django.core.mail import send_mail
from django.template import Context, Template, Engine
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from rest_framework_jwt.views import verify_jwt_token
from rest_framework_simplejwt.authentication import JWTAuthentication



User = get_user_model()



@api_view(["POST"])
def refresh_token(request):
    user = None
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        user_id = int(serializer.validated_data.get("user_id"))
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "user with id does not exist"}, status=status.HTTP_404_NOT_FOUND)
        try:
            old_refresh = RefreshToken(serializer.validated_data.get("refresh"))
        except TokenError as err:
            return Response(err.args, status=status.HTTP_400_BAD_REQUEST)
        if getattr(api_settings, 'ROTATE_REFRESH_TOKENS', False):
            if getattr(api_settings, 'BLACKLIST_AFTER_ROTATION', False):
                try:
                    old_refresh.blacklist()
                except AttributeError:
                    print("error in blacklisting token")
                    pass
        refresh = create_access_refresh_jwt_token(user)
        response = {
            "user_id": user_id,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        return Response(data=response, status=status.HTTP_200_OK)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["POST"])
def confirm_email(request):
    token = request.data.get("token")
    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    try:
        user = User.objects.get(id=decoded_token.get("id"))

        if not user:
            raise User.DoesNotExist()
        user.emailConfirmed = True
        user.save()
        return Response({"message": "Email confirmed"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "user with id does not exist"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def resendConfirm_email(request):
    token = request.data.get("token")
    decoded_token = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    try:
        user = User.objects.get(id=decoded_token.get("id"))
        if not user:
            raise User.DoesnotExist()
        if not user.emailConfirmed:
            user.emailConfirmed = True
            user.save()
            return Response({"message": "Email confirmed"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Email already confirmed"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "user with id does not exist"}, status=status.HTTP_404_NOT_FOUND)

    


@api_view(["POST"])
def forgot_password(request):
    serializer = UserForgotPassword(request.data)
    if serializer.is_valid():
        user = None
        try:
            user = User.objects.get(Q(email__exact=serializer.validated_data.get("email", None)))
        except User.DoesNotExist:
            return Response({"error": "user with this email does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        # send mail
        try:
            token = create_jwt_token(user)
            engine = Engine.get_default()
            template = engine.get_template("resetPasswordEmail.html")
            context = Context({ "user": user,
                                "resetPasswordEmailUrl": "http://localhost:8000/api/resetPassword/{}".format(token)})
            template_str = template.render(context)
            send_mail("resetPassword", "resetPassword message", os.getenv("SENDER_MAIL"),
                        [user.email], html_message=template_str)
        except Exception as err:
            print("error", err.args)
        return Response({"message": "email sent"}, status=status.HTTP_200_OK)
    else:
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(["POST"])
def reset_password(request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = None
            user_id = int(serializer.validated_data.get("user_id"))
            password = serializer.validated_data.get("newPassword")
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "user with id does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SignupView(APIView):

    def post(self, request):
        """sign up a user"""
        serializer = SignUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            try:
                token = create_jwt_token(user)
                engine = Engine.get_default()
                template = engine.get_template("confirmEmail.html")
                context = Context({ "user": user,
                                   "confirmEmailUrl": "http://localhost:8000/api/confirmEmail/{}".format(token)})
                template_str = template.render(context)
                send_mail("confirmEmail", "confirmEmail message", os.getenv("SENDER_MAIL"),
                            [user.email], html_message=template_str)
            except Exception as err:
                print("error", err.args)
            response = {"message": "user created succefully", "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

    def post(self, request):
        """login a user and generate token"""
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():   
            try:
                user = authenticate(email=email, password=password)
            except ValueError:
                return Response({"error": "user with email does not exist"},
                                status=status.HTTP_404_NOT_FOUND)
            
            if not user:
                return Response({"error": "password does not match user email"},
                                status=status.HTTP_400_BAD_REQUEST)
            
            refresh = None
            if serializer.validated_data.get("rememberMe"):
                    refresh = create_access_refresh_jwt_token(user, life_time=timedelta(days=90))
            else:
                refresh = create_access_refresh_jwt_token(user)
            token = {"refresh": str(refresh),
                     "access": str(refresh.access_token)}
            return Response({"message": "Login successfull", "token": token},
                            status=status.HTTP_200_OK)
        else:
            print("error", serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)