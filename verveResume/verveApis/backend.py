from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from django.db.models import Q

class CustomEmailBackend(ModelBackend):

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        print("username", username)
        print("email", email)
        print("password", password)
        User = get_user_model()
        user = None

        try:

            user = User.objects.get(Q(email__exact=username))
        except User.DoesNotExist:
            try:
                user = User.objects.get(Q(email__exact=email))
            except User.DoesNotExist:
                return None

         
        if check_password(password, user.password):
            if user.is_staff and user.is_active:
                user.is_superuser = True
                user.save()
                return user
        return None


