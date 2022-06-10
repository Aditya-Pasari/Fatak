from django.urls import path
from account.api.views import(
	registration_view,
	registration_ref_code_view,
	ObtainAuthTokenView,
)


app_name = 'account'

urlpatterns = [

	path('register/', registration_view, name="register"),
	path('register/<str:ref_code>/', registration_view, name="register"),
	path('login/', ObtainAuthTokenView.as_view(), name="login"), 
]