from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model


class UserManager(BaseUserManager):

    def create_user(self, email=None, username=None, password=None, **kwargs):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(
            email=self.normalize_email(email)
            )
        
        if kwargs:
            for key, value in kwargs.items():
                setattr(user, key, value)
        
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email=None, password=None, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        user = self.create_user(
            email=email,
            password=password,
            **kwargs
        )
        
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user