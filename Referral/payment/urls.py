from django.urls import path
from . import views


urlpatterns = [
    
    path('razorpay/', views.razorpay_page, name="razorpay_page"),
    path('razorpay/paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('create_customer', views.create_customer, name = 'create_customer')
   ]
