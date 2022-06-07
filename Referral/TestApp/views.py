from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
import string
from random import choice, randrange
from TestApp.models import Referral, ReferralCode
from django.db.models import Sum
from django.utils import timezone
import datetime


# Create your views here.
def home(request):
    context = {}
    return render(request, 'home.html', context)


def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")
            print("User does not exist")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            print("User logging in")
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username and password do not match")

    context = {}
    return render(request, 'login.html', context)




def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

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
                messages.success(request, "You were referred by" + str(referralCode.referrer))
                messages.success(request, "You received Rs " + str(r.referee_amount))
            else:
                messages.success(request, "No referral code was used during user registration.")

            return redirect('home')
        else:
            print(form.errors.as_data())
            messages.error(request, "Error during registration")

    context = {'form': form}
    return render(request, 'register.html', context)



def logoutUser(request):
    logout(request)
    return redirect('home')




def getReferralCode(request):
    user = request.user
    print(str(user))
     
    if(ReferralCode.objects.filter(referrer=user).exists()):
        referral_code  = ReferralCode.objects.get(pk=user).referral_code
        messages.success(request, "Your existing Referral Code is : " + referral_code)
    else:
        referral_code = ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        r = ReferralCode(referrer = request.user, referral_code = referral_code)
        r.save()
        messages.success(request, "Your new Referral Code is : " + referral_code)



   
    return redirect('home')





