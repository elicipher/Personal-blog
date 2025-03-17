from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Member(AbstractUser):

    full_name = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to="avatar/" , blank=True , null=True , verbose_name='تصویر پروفایل')
    created_at = models.DateTimeField(auto_now_add=True , verbose_name='تاریخ عضویت')

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name  = "کاربر"
        verbose_name_plural = "کاربران"
    