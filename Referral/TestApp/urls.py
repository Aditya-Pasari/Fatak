

from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('get_ref_code/', views.getReferralCode, name="getReferralCode"),


    path('api/get_referral_code/<str:user>/', views.api_get_referral_code, name='api_get_referral_code'),
]
