from django.contrib import admin

from payment.models import RazorpayCustomer, RazorpayOrderID

# Register your models here.


admin.site.register(RazorpayCustomer)
admin.site.register(RazorpayOrderID)
