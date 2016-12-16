from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from wallet.models import Wallet, Userprofile
from django.http import HttpResponseRedirect
from wallet.forms import UserReg


def user_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # if request.POST['next']:
                #     return HttpResponseRedirect(request.POST['next'])
                # else:
                #     return render(request, '/user_profile.html/', {'user': user, 'wallet': user.userprofile.wallet_id})
            else:
                return render(request, 'registration/login.html/', {'error': 'User is not active'})
        else:
            return render(request, 'registration/login.html/', {'error': 'User does not exist'})
    else:
        return render(request, 'registration/login.html/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('home.html')


def create_user(request):
    form = UserReg(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        wallet = Wallet(username=request.POST['username'], amount=0)
        wallet.save()
        user.save()
        userprofile = Userprofile(user=user, wallet_id=wallet)
        userprofile.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return render(request, 'user_profile.html', {'user': user, 'wallet': wallet})
    context = {
        "form": form,
    }
    return render(request, 'create_user.html',context)


def home(request):
    return render(request, 'home.html')
