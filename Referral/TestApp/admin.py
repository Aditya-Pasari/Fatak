from django.contrib import admin
from .models import ReferralCode, Referral

# Register your models here.

class ReferralCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

admin.site.register(ReferralCode, ReferralCodeAdmin)
admin.site.register(Referral)