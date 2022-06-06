from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm



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
            return redirect('home')
        else:
            messages.error(request, "Error during registration")

    context = {'form': form}
    return render(request, 'register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


