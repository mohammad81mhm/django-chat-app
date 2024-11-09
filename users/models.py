from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number_validator = RegexValidator(
        regex=r'^\d{11}$',
        message='شماره موبایل باید دقیقا ۱۱ رقم باشد.',
        code='invalid_phone_number'
    )

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[phone_number_validator],
    )
    username = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    last_login = None
    is_superuser = None
    is_staff = None
    password = None

    def __str__(self):
        return self.phone_number


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
