from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Member(AbstractUser):

    full_name = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to="avatar/" , blank=True , null=True , verbose_name='تصویر پروفایل')


    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name  = "کاربر"
        verbose_name_plural = "کاربران"
    