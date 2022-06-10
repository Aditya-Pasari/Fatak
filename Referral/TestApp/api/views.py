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
import datetime




#########################################################################################
################################# APIs ##################################################
#########################################################################################


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_referral_code(request, user):
    try:
        referralCode = ReferralCode.objects.get(referrer=user)
        serializer = ReferralCodeSerializer(instance=referralCode)
        
        return Response(serializer.data)
    except ReferralCode.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_referral(request, referee):
    try:
        referral = Referral.objects.get(referee=referee)
        
        created_time = referral.created
        updated_time = referral.updated


        timediff = (updated_time - created_time)
        timediff_hours = round(timediff.total_seconds()/(60*60),1)
        print("Time for first transaction = " + str(timediff_hours))
        serializer = ReferralSerializer(instance=referral)
        return Response(serializer.data)
    except:
        response = {
                "referee": referee,
                "referrer_amount": 0,
                "referee_amount": 0,
                "referrer": None
                }
        return Response(response)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def api_get_referrer_stats(request, referrer):
    #try:   
        five_minutes_ago = timezone.now() + datetime.timedelta(minutes=-5)
        amount_earned__current_month = Referral.objects.filter(created__gte=five_minutes_ago).filter(referrer=referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']
        if(amount_earned__current_month is None):
            amount_earned__current_month = 0
        total_amount_earned = Referral.objects.filter(referrer=referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']
        if(total_amount_earned is None):
            total_amount_earned = 0
 
        return Response({'amount_earned__current_month': amount_earned__current_month,
                        'total_amount_earned': total_amount_earned})
    

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
        return Response({'message':'User successfully carried out first transaction'})
    except:
        return Response({'message':'User didnt use Referral Code'})


#########################################################################################
############################# END OF  APIs ##############################################
#########################################################################################


