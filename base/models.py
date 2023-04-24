from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime

class Post(models.Model):
    title = models.CharField(max_length=200, default='')
    kontenti = models.CharField(max_length=200, default='')
    ball = models.CharField(max_length=200, default='bal')

class Color(models.Model):
    name = models.CharField(max_length=20)
    pastel = models.BooleanField(default=False)

    def __str__(self):
        return self.name
        
class Event(models.Model):
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)

    start = models.IntegerField(validators=[MaxValueValidator(96), MinValueValidator(0)])
    end = models.IntegerField(validators=[MaxValueValidator(96), MinValueValidator(0)])
    date = models.DateField(default=datetime.date.today)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=30, default='')
    password = models.CharField(max_length=20)
    bio = models.CharField(max_length=250)
    age = models.IntegerField(null=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['bio']

    objects = CustomUserManager()
