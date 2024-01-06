from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Template

class UserSerializer(serializers.ModelSerializer):

    templates = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='template-detail'
    )

    class Meta:
        model = User
        fields = ["id", "email", "phoneNumber", "first_name", "last_name", "createdAt", "updatedAt", "templates", "date_of_birth"]
        read_only_fields = ['createdAt', 'updatedAt']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        read_only_fields = ['createdAt', 'updatedAt']




