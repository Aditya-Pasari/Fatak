from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.
class ReferralCode(models.Model):
    referrer = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,  primary_key=True)
    referral_code = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Referral(models.Model):
    referrer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+')
    referee  = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    referrer_amount = models.IntegerField()
    referee_amount = models.IntegerField()                           # Select random amount upto Rs 50
    first_transaction = models.BooleanField(default=False)                             

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

