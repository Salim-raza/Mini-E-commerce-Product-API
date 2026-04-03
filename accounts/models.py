from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings
from django.db import models
import datetime

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICE = (
        ("ADMIN", "Admin"),
        ("CUSTOMER", "Customer")
    )
    role = models.CharField(choices=ROLE_CHOICE, default="customer")
    phone = models.CharField(unique=True)

class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)    
    
    
    def is_expired(self):
        print ("created_at", self.created_at)
        print("expired_at", timezone.now() + datetime.timedelta(hours=1))
        
        return self.created_at + datetime.timedelta(hours=1) > timezone.now()