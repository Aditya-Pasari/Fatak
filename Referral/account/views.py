from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm

import string
from random import choice, randrange
from TestApp.models import Referral, ReferralCode
from django.db.models import Sum
from django.utils import timezone
import datetime
from django.contrib import messages


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            
            ref_code = request.POST.get('ref_code')
            if(ref_code):
                print("Ref Code = " + str(ref_code))

                referralCode = ReferralCode.objects.get(referral_code= ref_code)

                five_minutes_ago = timezone.now() + datetime.timedelta(minutes=-5)
                user_amount = Referral.objects.filter(created__gte=five_minutes_ago).filter(referrer=referralCode.referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']
                total_user_amount = Referral.objects.filter(referrer=referralCode.referrer).aggregate(Sum('referrer_amount'))['referrer_amount__sum']
                #total_users_referred = 
                
                if(user_amount is None):
                    user_amount = 0

                if(total_user_amount is None):
                    total_user_amount = 0

                
                
                referrer_amount = 30 if user_amount < 150 else 0
                

                r = Referral(referrer = referralCode.referrer, 
                            referee = request.user,
                            referrer_amount = referrer_amount,
                            referee_amount = randrange(50)
                        )
                r.save()
                messages.success(request, "Total amount received by Original referrer in last 5 minutes is Rs " + str(user_amount + referrer_amount))
                messages.success(request, "Total amount received by Original referrer uptil now is Rs : " + str(total_user_amount + referrer_amount)) 
                messages.success(request, "You were referred by " + str(referralCode.referrer))
                messages.success(request, "You received Rs " + str(r.referee_amount))
            else:
                messages.success(request, "No referral code was used during user registration.")
           

            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register1.html', context)


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "login1.html", context)


def account_view(request):

    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(

            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )

    context['account_form'] = form

    return render(request, "account.html", context)


def must_authenticate_view(request):
    return render(request, 'must_authenticate.html', {})
