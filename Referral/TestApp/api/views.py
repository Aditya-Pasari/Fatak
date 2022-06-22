from time import time
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status


from TestApp.models import Referral, ReferralCode
from TestApp.serializers import ReferralCodeSerializer, ReferralSerializer

from django.db.models import Sum
from django.utils import timezone
import datetime, string
from random import choice

from account.models import Account

#########################################################################################
################################# APIs ##################################################
#########################################################################################


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_referral_code(request, user):
    if(ReferralCode.objects.filter(referrer=user).exists()):
        r  = ReferralCode.objects.get(referrer=user)
    else:
        ref_code = ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        account_user = Account.objects.get(pk = user)
        r = ReferralCode(referrer = account_user, referral_code = ref_code)
        r.save()
        
    serializer = ReferralCodeSerializer(instance=r)
        
    return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'Referral code sent successfully',
                    'data': serializer.data
                    },
                    status = status.HTTP_200_OK)

        



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_referral(request, referee):
    try:
        referral = Referral.objects.get(referee=referee)
        
        #created_time = referral.created
        #updated_time = referral.updated
        #timediff = (updated_time - created_time)
        #timediff_hours = round(timediff.total_seconds()/(60*60),1)
        #print("Time for first transaction = " + str(timediff_hours))
        serializer = ReferralSerializer(instance=referral)
        return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'Referral sent successfully',
                    'data': serializer.data
                    },
                    status = status.HTTP_200_OK)
    except:
        data = {
                "referee": referee,
                "referrer_amount": 0,
                "referee_amount": 0,
                "referrer": None
                }
        return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': "User didn't use referral code",
                    'data': data
                    },
                    status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_referrer_stats(request, referrer):
    #try:   
        five_minutes_ago = timezone.now() + datetime.timedelta(minutes=-5)
        amount_earned_current_month = Referral.objects.filter(created__gte=five_minutes_ago).filter(referrer=referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']
        
        if(amount_earned_current_month is None):
            amount_earned_current_month = 0
        
        total_amount_earned = Referral.objects.filter(referrer=referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']

        if(total_amount_earned is None):
            total_amount_earned = 0

        data = {'amount_earned_current_month': amount_earned_current_month,
                        'total_amount_earned': total_amount_earned}
        return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'Referrer stats sent successfully',
                    'data': data
                    },
                    status = status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_all_referrers(request):
    queryset = Referral.objects.all()

    five_minutes_ago = timezone.now() + datetime.timedelta(minutes=-5)

    queryset_month = Referral.objects.filter(created__gte=five_minutes_ago)

    all_users = {}

    for q in queryset:
        if(q.referrer.id in all_users):
            all_users[q.referrer.id]['users_registered'] += 1
            all_users[q.referrer.id]['total_amount'] += q.referrer_amount
        else:
            all_users[q.referrer.id] = {}
            all_users[q.referrer.id]['users_registered'] = 1
            all_users[q.referrer.id]['users_registered_this_month'] = 0
            all_users[q.referrer.id]['total_amount'] = q.referrer_amount

    for q in queryset_month:
        all_users[q.referrer.id]['users_registered_this_month'] +=  1



    response_dict = dict(sorted(all_users.items(), key=lambda item: -item[1]['users_registered']))


    return JsonResponse(response_dict)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def api_make_transaction(request, referee):

    try:
        r = Referral.objects.get(referee = referee)
        
        if(not r.first_transaction):    
            r.first_transaction = True
            r.save() 
        return Response({
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'User successfully carried out first transaction',
                    'data': None,
                    },
                    status = status.HTTP_200_OK)
    except:
        return Response({
                    'success': False,
                    'status_code': status.HTTP_400_BAD_REQUEST,
                    'message': 'User didnt use Referral Code',
                    'data': None,
                    },
                    status = status.HTTP_400_BAD_REQUEST)


#########################################################################################
############################# END OF  APIs ##############################################
#########################################################################################


