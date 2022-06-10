from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from account.api.serializers import RegistrationSerializer
from account.models import Account
from rest_framework.authtoken.models import Token


from random import randrange
from TestApp.models import Referral, ReferralCode
from django.db.models import Sum
from django.utils import timezone
import datetime


# Url: https://<your-domain>/api/account/register
@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_view(request, ref_code = None):

	if request.method == 'POST':
        #print("Entering register API")
		data = {}
		email = request.data.get('email', '0').lower()
		if validate_email(email) != None:
			data['error_message'] = 'That email is already in use.'
			data['response'] = 'Error'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['error_message'] = 'That username is already in use.'
			data['response'] = 'Error'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)
		
		if serializer.is_valid():
			account = serializer.save()
			data['response'] = 'successfully registered new user.'
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk

			if(ref_code is None):
				ref_code = request.data.get('ref_code')

			if(ref_code):
				referralCode = ReferralCode.objects.get(referral_code= ref_code)
				
				five_minutes_ago = timezone.now() + datetime.timedelta(minutes=-5)
				#user_amount = Referral.objects.filter(created__gte=five_minutes_ago).filter(referrer=referralCode.referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']
				#total_user_amount = Referral.objects.filter(referrer=referralCode.referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']
                
				#if(user_amount is None):
				#	user_amount = 0
				
				#if(total_user_amount is None):
				#	total_user_amount = 0

				#referrer_amount = 30 if user_amount < 150 else 0

				user_count = Referral.objects.filter(created__gte=five_minutes_ago).filter(referrer=referralCode.referrer).count()
				referrer_amount = randrange(50) if user_count < 5 else 0
                
				r = Referral(referrer = referralCode.referrer, 
                            referee = account,
                            referrer_amount = referrer_amount,
                            referee_amount = randrange(50)
                        )
				r.save()
			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)

@api_view(['POST', ])
@permission_classes([])
@authentication_classes([])
def registration_ref_code_view(request, ref_code):

	print("Entering here")
	return Response({"message" : "success", "ref_code" : ref_code})


def validate_email(email):
	account = None
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		return None
	if account != None:
		return email

def validate_username(username):
	account = None
	try:
		account = Account.objects.get(username=username)
	except Account.DoesNotExist:
		return None
	if account != None:
		return username



# URL: http://127.0.0.1:8000/api/account/login
class ObtainAuthTokenView(APIView):

	authentication_classes = []
	permission_classes = []

	def post(self, request):
		context = {}

		email = request.POST.get('username')
		password = request.POST.get('password')
		account = authenticate(email=email, password=password)
		if account:
			try:
				token = Token.objects.get(user=account)
			except Token.DoesNotExist:
				token = Token.objects.create(user=account)
			context['response'] = 'Successfully authenticated.'
			context['pk'] = account.pk
			context['email'] = email.lower()
			context['token'] = token.key
		else:
			context['response'] = 'Error'
			context['error_message'] = 'Invalid credentials'

		return Response(context)