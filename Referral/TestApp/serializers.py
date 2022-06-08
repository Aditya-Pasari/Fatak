
from rest_framework import serializers
from .models import ReferralCode
from django.contrib.auth import get_user_model

class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id','username')

        