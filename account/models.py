from django.db import models
from core.models import TimeStamp
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from .constant import GENDER_TYPE
# Create your models here.
class User(AbstractUser, TimeStamp):
    email = models.EmailField(unique = True)
    phone = models.CharField(max_length = 15, default='')
    gender = models.CharField(max_length=8, choices=GENDER_TYPE)
    
    objects = UserManager()
    REQUIRED_FIELDS = ('email',)

    def __str__(self) -> str:
        return self.username