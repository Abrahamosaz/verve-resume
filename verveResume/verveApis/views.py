from django.shortcuts import render
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (UserSerializer, TemplateSerializer)
from rest_framework import status
from django.contrib.auth import get_user_model
from  django.db.models import Q
import jwt


# Create your views here.

class SignUp(APIView):

    def post(self, request, format=None):
        User = get_user_model()
        data = request.data
        serializer = UserSerializer(data = data)
        if serializer.is_valid():
            user = User.objects.get(Q(email__exact = data.get("email", None)))
            
            if user:
                return Response({"message": "User already exits"}, status=status.HTTP_400_BAD_REQUEST)

            user = User(**serializer.validated_data)
            payload = {
                "id": user.id,
                "email": user.email,
            }

            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

            if not token:
                return Response({"message": "Error generationg token"}, status=status.HTTP_400_BAD_REQUEST)






    

class getUser(APIView):

    def get(self, request):
        User = get_user_model()

        users = []

        for user in User.objects.all():
            users.append(UserSerializer(user).data)
        if users:
            return Response(users, status=status.HTTP_200_OK)
        return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)





