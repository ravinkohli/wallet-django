from wallet.models import *
import datetime
from django.views.decorators.csrf import csrf_exempt


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
            return {"status": True}
    else:
        return {"status": False, "errors": "Missing content"}
