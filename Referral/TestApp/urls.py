

from django.urls import path
from . import views


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import MyTokenObtainPairView



urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('get_ref_code/', views.getReferralCode, name="getReferralCode"),

    path('api/get_referral_code/<str:user>/', views.api_get_referral_code, name='api_get_referral_code'),
    path('api/get_referral/<str:referee>/', views.api_get_referral, name='api_get_referral'),
    path('api/get_referrer_stats/<str:referrer>/', views.api_get_referrer_stats, name='api_get_referrer_stats'),

    # Token URLS
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/mytoken/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
