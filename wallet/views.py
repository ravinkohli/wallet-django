from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.contrib import messages
from datetime import datetime
from wallet.serialisers import *
from wallet.forms import UserForm, ProfileForm
from rest_framework import generics
from wallet.authorisations import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework import status
from update_functions import *
from rest_framework.parsers import JSONParser

# Create your views here.


def receive_money(request):
    username = request.GET.get("username", None)
    amount = request.GET.get("amount", None)
    wallet = Wallet.objects.get(username=username)
    wallet.add_money(int(amount))
    wallet.save()
    wallet = Wallet.objects.get(username=request.user.username)
    return render(request, 'user_profile.html', {'user': request.user,'userprofile': Userprofile.objects.get(user=request.user), 'wallet': wallet})


def add_money(request):
    if request.user:
        if request.POST and request.POST.get('amount'):
            username = request.user.username
            add_amount = request.POST.get('amount')
            wallet = Wallet.objects.get(username=username)
            wallet.add_money(add_amount)
            wallet.save()
            now = datetime.datetime.now()
            trans = Transaction(from_name=username, wallet_id=wallet, date=now, amount=add_amount)
            trans.save()
            return render(request, 'user_profile.html', {'user': request.user,'userprofile': Userprofile.objects.get(user=request.user), 'wallet': wallet})
        else:
            return render(request, 'add_money.html')
    else:
        return HttpResponseRedirect('/login/?next={}'.format('/add_money/'))


def subtract_money(request):
    """
    Used to send money
    :param request:
    :return:
    """
    if request.user:
        users = User.objects.all()
        users_ids = users.values_list('id', flat=True)
        users_list = []
        for id in users_ids:
            user = users.get(pk=id)
            if user.username != "ravinkohli" and user.username != request.user.username:
                users_list.append(user)
        if request.POST and request.POST.get('amount'):
            username = request.user.username
            withdraw = request.POST.get('amount')
            wallet = Wallet.objects.get(pk=request.user.userprofile.wallet_id_id)
            if int(withdraw) > int(wallet.amount):
                return render(request, 'send_money.html', {'error': 'Amount can not be greater than balance','users': users_list})
            wallet.subtract_money(withdraw)
            wallet.save()
            now = datetime.datetime.now()
            trans = Transaction(from_name=username, wallet_id=wallet,to=request.POST.get('receiver'), date=now, amount=withdraw)
            trans.save()
            # print request.POST.get('receiver')
            return redirect('/receive/?username=%s&amount=%s' % (request.POST.get('receiver'), withdraw))
        else:
            return render(request, 'send_money.html',{'users': users_list})
    else:
        return HttpResponseRedirect('/login/?next={}'.format('/subtract_money/'))


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        wallet = Wallet.objects.filter(username=request.user.username)
        request.user.userprofile.wallet_id = wallet.get()
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('/accounts/profile/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def user_profile(request):
    context = {}
    context['name'] = request.user.first_name + request.user.last_name
    context['wallet'] = request.user.userprofile.wallet_id
    context['transactions'] = Transaction.objects.filter(wallet_id=request.user.userprofile.wallet_id)
    if request.user.userprofile.date_ob:
        context['dob'] = request.user.userprofile.date_ob
    if request.user.userprofile.sex:
        context['sex'] = request.user.userprofile.sex
    return render(request, 'user_profile.html', context)


@login_required
def transaction(request):
    context = {}
    trans = Transaction.objects.filter(from_name=request.user.username)
    context['transaction'] = trans
    context['user'] = request.user
    return render(request, 'transaction.html', context)


# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)
#


class WalletList(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        wallet = Wallet.objects.filter(id=request.user.userprofile.wallet_id_id)
        serializer = WalletSerializer(wallet, many=True)
        print("Serializer: %s", serializer.data)
        return Response(serializer.data)


class TransactionDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        wallet_id = request.user.userprofile.wallet_id_id
        transactions = Transaction.objects.filter(wallet_id=wallet_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        add_transaction(request, data)
        return Response(status=status.HTTP_200_OK)


class UserDetail(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        userprofile = Userprofile.objects.get(user_id=request.user.id)
        serializer = UserProfileSerializer(userprofile)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        data = JSONParser().parse(request)
        update_userprofile(request, data)
        return Response({"errors": "No errors"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated, ])
def add_money_api(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        wallet = Wallet.objects.get(username=request.user.username)
        if data["amount"]:
            wallet.add_money(data["amount"])
            wallet.save()
            trans = Transaction(from_name=request.user.username, wallet_id=wallet, date=datetime.datetime.now(), amount=data["amount"], to="self")
            trans.save()
            return Response({"errors": "No errors"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"errors": "Amount not specified"}, status=status.HTTP_206_PARTIAL_CONTENT)


@api_view(["POST"])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated, ])
@csrf_exempt
def send_money(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        success = send_money_api(request, data)
        if success["status"]:
            return Response({"errors": "No errors"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"errors": success["errors"]}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
@csrf_exempt
def get_all_sessions(request):
    if request.method == "GET":
        tokens = DeviceToken.objects.filter(user=request.user)
        sessions = []
        for token in tokens:
            if token.expired():
                continue
            session = {}
            session["token"] = token.key
            session["device"] = token.device_browser
            session["created"] = token.created
            session["expiry"] = token.expired_date
            sessions.append(session)
        return Response({"sessions": sessions}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([TokenAuthentication,])
@permission_classes([IsAuthenticated,])
@csrf_exempt
def get_users(request):
    users = User.objects.all()
    all_users = []
    for user in users:
        if user != request.user and not user.is_staff:
            all_users.append([user.username])
    return Response({"errors": "No Errors", "users": all_users}, status=status.HTTP_200_OK)
