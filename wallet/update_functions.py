from wallet.models import *
import datetime
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST


def add_transaction(request, data):
    wallet = Wallet.objects.get(username=request.user.username)
    transaction = Transaction(from_name=request.user.username, wallet_id=wallet, date=data["date"], to=data['to'], amount=data["amount"])
    transaction.save()


def update_userprofile(request, data):
    userprofile = Userprofile.objects.get(user_id=request.user.id)
    if data["date_ob"]:
        userprofile.date_ob = data["date_ob"]
    if data["sex"]:
        userprofile.sex = data["sex"]
    userprofile.save()
    if data["email"]:
        request.user.email = data["email"]
    request.user.save()


def create_user_api(data):
    if data["username"] and data["password"]:
        user = User(username=data["username"], password=data["password"])
        user.set_password(data["password"])
        try:
            user.save()
        except:
            return {"status": False, "errors": "Username already exists"}
        wallet = Wallet(username=user.username, amount=0)
        wallet.save()
        userprofile = Userprofile(user=user, wallet_id=wallet)
        userprofile.save()
        return {"status": True}
    else:
        return {"status": False}


@csrf_exempt
def send_money_api(request, data):
    if data["amount"] and data["to"]:
        wallet = Wallet.objects.get(username=request.user.username)
        users = User.objects.all()
        users_names = []
        for user in users:
            users_names.append(user.username)
        user = User.objects.filter(is_staff=True)
        admin_names = []
        for admin in user:
            admin_names.append(admin.username)
        if int(data["amount"]) > int(wallet.amount):
            return {"status": False, "errors": "Withdraw amount greater than balance"}
        elif data["to"] in admin_names and data["to"] == request.user.username and data["to"] not in users_names:
            return {"status": False, "errors": "Invalid recipient"}
        else:
            wallet.subtract_money(data["amount"])
            wallet.save()
            transaction = Transaction(from_name=request.user.username, wallet_id=wallet, date=datetime.datetime.now(),
                                      to=data['to'], amount=data["amount"])
            transaction.save()
            wallet = Wallet.objects.get(username=data["to"])
            wallet.add_money(data["amount"])
            wallet.save()
            return {"status": True}
    else:
        return {"status": False, "errors": "Missing content"}


"""Utility views for Expiring Tokens.
Classes:
    ObtainExpiringAuthToken: View to provide tokens to clients.
"""


class ObtainExpiringAuthToken(ObtainAuthToken):

    """View enabling username/password exchange for expiring token."""

    model = DeviceToken

    def post(self, request, *args, **kwargs):
        """Respond to POSTed username/password with token."""
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            token, created = DeviceToken.objects.get_or_create(user=serializer.validated_data['user'], device_browser=(request.user_agent.browser.family+
                                                                                                              request.user_agent.os.family))

            token.is_active = True
            token.save()
            if token.expired():
                # If the token is expired, generate a new one.
                token = DeviceToken.objects.create(
                    user=serializer.validated_data['user'],
                    device_browser=(request.user_agent.browser.family +
                                    request.user_agent.os.family)
                )
                token.is_active = True
                token.save()
            data = {'token': token.key}
            return Response(data)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()
