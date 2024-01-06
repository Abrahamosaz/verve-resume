from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password


class MyUserBackend(ModelBackend):

    def authenticate(self, request, username=None, email=None, password=None):
        User = get_user_model()
        user = None

        if username is not None:
            try:
                user = User.objects.get(Q(email__iexact=username))
            except User.DoesNotExist:
                pass

        if user is None and email is not None:
            try:
                user = User.objects.get(Q(email__iexact=email))
            except User.DoesNotExist:
                raise ValueError()

        if user and user.check_password(password):
            if user.is_active:
                return user
        return None
    

