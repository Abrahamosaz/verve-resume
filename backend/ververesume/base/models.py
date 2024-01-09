from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from .manager import UserManager


def user_template_path(instance, filename):
    return "user_{0}/{1}".format(instance.user.id, filename)


class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phoneNumber = models.CharField(max_length=20, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    emailConfirmed = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        ordering = ["-createdAt"]
        db_table = "user_table"

    def __str__(self):
        return self.email
    

class Template(models.Model):
    template_file = models.FileField(upload_to=user_template_path)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(get_user_model(), related_name="templates", on_delete=models.CASCADE)


    class Meta:
        ordering = ["createdAt", "updatedAt"]
        db_table = "template_table"

    def __str__(self):
        return "template_{}".format(self.id)


