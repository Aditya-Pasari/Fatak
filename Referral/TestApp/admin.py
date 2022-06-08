from django.contrib import admin
from .models import ReferralCode, Referral
from django.contrib.auth.models import User

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'id')
    readonly_fields = ('id',)

class ReferralCodeAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')



admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(ReferralCode, ReferralCodeAdmin)
admin.site.register(Referral)