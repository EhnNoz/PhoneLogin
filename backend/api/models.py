from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.hashers import make_password


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    username = models.CharField(max_length=150, unique=False)  # غیر منحصر به فرد
    # username = None
    USERNAME_FIELD = 'phone_number'
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_expiry = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number

    def set_verification_code(self, code):
        self.verification_code = code
        # زمان انقضای کد تأیید را 5 دقیقه بعد تنظیم کنید
        self.verification_code_expiry = timezone.now() + timedelta(minutes=5)
        self.set_password(code)
        # self.username(self.phone_number)
        self.save()


    # @staticmethod
    # def generate_password(phone_number):
    #     return f"password_{phone_number}"
    #
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.password = make_password(self.generate_password(self.phone_number))
    #         self.username = self.phone_number
    #     super().save(*args, **kwargs)
