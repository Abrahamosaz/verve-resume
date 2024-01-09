from django.contrib.auth import get_user_model
from  base.models import Template
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.serializers import ValidationError
from django.db.models import Q


User = get_user_model()


class TokenSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    refresh = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    rememberMe = serializers.BooleanField(write_only=True, default=False)




class UserForgotPassword(serializers.Serializer):
    email = serializers.EmailField()

        

class ResetPasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(write_only=True)
    newPassword = serializers.CharField(write_only=True)
    confirmNewPassword = serializers.CharField(write_only=True)


    def validate(self, attrs):

        newPassword = attrs.get("newPassword")
        confirmNewPassword = attrs.get("confirmNewPassword")

        if newPassword != confirmNewPassword:
            raise ValidationError("passwords does not match")
        return super().validate(attrs)


class SignUserSerializer(serializers.ModelSerializer):
    confirmPassword = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all(),
                                                               message="user with email already exists")])

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "createdAt",
                  "updatedAt", "templates", "password", "confirmPassword"]
        extra_kwargs = {
            "password": {"write_only": True},
            "templates": {"read_only":True}
        }

    def validate(self, attrs: dict):
        # Apply custom validation either here
        password = attrs.get("password")
        confirmPassword = attrs.get("confirmPassword")

        if password != confirmPassword:
            raise ValidationError("passwords does not match")

        attrs.pop("confirmPassword")
        return super().validate(attrs)


    def create(self, validated_data: dict) -> User:
        password = validated_data.get("password", None)
        user = User(**validated_data)

        user.set_password(password)
        user.save()
        return user
        


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = "__all__"
        




