

from django.urls import path
from . import views



urlpatterns = [
    
    path('login1/', views.login_view, name="login"),
    path('register1/', views.registration_view, name="register"),
    path('logout1/', views.logout_view, name="logout"),
    path('account/', views.account_view, name="account"),

   ]
