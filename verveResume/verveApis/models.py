from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, date_of_birth, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        
        if not email:
            raise ValueError("users must have an email address")
        
        user = self.model(
            email = self.normalize_email(email),
            date_of_birth = date_of_birth
            )
        
        if extra_fields:
            for key, value in extra_fields.items():
                setattr(user, key, value)

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, date_of_birth, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user



class User(AbstractUser):

    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    phoneNumber = models.CharField(max_length=255, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['password', 'date_of_birth']

    objects = UserManager()


    class Meta:
        db_table = "user_table"
        ordering = ["-createdAt"]

    
    def __str__(self):
        return self.email



class Template(models.Model):
    template_file = models.FileField(upload_to="upload", blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, related_name="templates", on_delete=models.CASCADE)

    class Meta:
        db_table = "templates_table"
        ordering = ["-createdAt"]





