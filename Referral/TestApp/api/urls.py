from django.urls import path
from . import views


app_name = 'TestApp'

urlpatterns = [
    path('get_referral_code/<str:user>/', views.api_get_referral_code, name='api_get_referral_code'),
    path('get_referral/<str:referee>/', views.api_get_referral, name='api_get_referral'),
    path('get_referrer_stats/<str:referrer>/', views.api_get_referrer_stats, name='api_get_referrer_stats'),
    path('get_all_referrers/', views.api_get_all_referrers, name='api_get_all_referrers'),
    path('make_transaction/<str:referee>/', views.api_make_transaction, name="api_make_transaction"),

]