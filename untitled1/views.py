from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from wallet.models import Wallet, Userprofile, Transaction, DeviceToken
from django.http import HttpResponseRedirect
from wallet.forms import UserReg
from django.views.decorators.csrf import csrf_exempt
from wallet.authorisations import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from wallet.update_functions import create_user_api
import datetime


def user_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # token = Token.objects.create(user=user)
                # token.save()
                # if request.POST['next']:
                #     return HttpResponseRedirect(request.POST['next'])
                # else:
                #    return render(request, '/user_profile.html/', {'user': user, 'wallet': user.userprofile.wallet_id})
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


@api_view(["GET"])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated, ])
def logout(request):
    if request.user and request.method == "GET":
        token = DeviceToken.objects.get(user=request.user, device_browser=(request.user_agent.browser.family+
                                                                           request.user_agent.os.family))
        token.expired_date = datetime.datetime.now()
        token.is_active = False
        token.save()
        return Response({"errors": "No error"}, status=status.HTTP_200_OK)
    else:
        return Response({"errors": "User invalid or wrong API request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([])
@permission_classes([])
@csrf_exempt
def createuser(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        success = create_user_api(data)
        if success["status"]:
            return Response({"errors": "No error"}, status=status.HTTP_201_CREATED)
        elif success["errors"]:
            return Response({"errors": success["errors"]}, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)


