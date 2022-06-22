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
		data = {}
		email = request.data.get('email', '0').lower()
		if validate_email(email) != None:
			data['success'] = False
			data['message'] = 'That email is already in use.'
			return Response(data)

		username = request.data.get('username', '0')
		if validate_username(username) != None:
			data['success'] = False
			data['message'] = 'That username is already in use.'
			return Response(data)

		serializer = RegistrationSerializer(data=request.data)
		
		if serializer.is_valid():

			if(ref_code is None):
				ref_code = request.data.get('ref_code')

			if(ref_code):
				if(ReferralCode.objects.filter(referral_code= ref_code).exists()):
					referralCode = ReferralCode.objects.get(referral_code= ref_code)
				
					five_minutes_ago = timezone.now() + datetime.timedelta(minutes=-5)		# For checking how many referee's used referrers code this month
					user_amount = Referral.objects.filter(created__gte=five_minutes_ago).filter(referrer=referralCode.referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']
				
					if(user_amount is None):
						user_amount = 0
					referrer_amount = 30 if user_amount < 150 else 0

					# NOT REQUIRED HERE
					#total_user_amount = Referral.objects.filter(referrer=referralCode.referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']
					#if(total_user_amount is None):
					#	total_user_amount = 0

					# USE THIS when want to randomize amount received by REFERRER too.
					#user_count = Referral.objects.filter(created__gte=five_minutes_ago).filter(referrer=referralCode.referrer).count()
					#referrer_amount = randrange(50) if user_count < 5 else 0
					account = serializer.save()
					data['message'] = 'Successfully registered new user with referral code.'

					r = Referral(referrer = referralCode.referrer, 
                            referee = account,
                            referrer_amount = referrer_amount,
                            referee_amount = randrange(50)
                        )
					r.save()	
				else:
					data['success'] = False
					data['message'] = 'Referral code is incorrect. Please enter correct referral code.'
					return Response(data)
			else:
				account = serializer.save()
				data['message'] = 'Successfully registered new user without referral code.'
				
			
			data['email'] = account.email
			data['username'] = account.username
			data['pk'] = account.pk

			token = Token.objects.get(user=account).key
			data['token'] = token
		else:
			data = serializer.errors
		return Response(data)


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