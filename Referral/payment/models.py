import email
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class RazorpayCustomer(models.Model):
    createdby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id      = models.CharField(max_length=30, primary_key=True)
    name    = models.CharField(max_length=255)
    email   = models.CharField(max_length=255)
    contact = models.CharField(max_length=10)
    gstin   = models.CharField(max_length=255, blank=True)
    notes1  = models.CharField(max_length=255)
    notes2  = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class RazorpayOrderID (models.Model):
    payer       =   models.CharField(max_length=25)
    receiver    =   models.CharField(max_length=25)
    order_id    =   models.CharField(max_length=25)
    amount      =   models.IntegerField()
    amount_paid =   models.IntegerField()
    amount_due  =   models.IntegerField()
    currency    =   models.CharField(max_length=10, default = 'INR')
    status      =   models.CharField(max_length=255)
    notes1  = models.CharField(max_length=255)
    notes2  = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



class RazorpayPayment(models.Model):
    pass