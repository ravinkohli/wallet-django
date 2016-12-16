from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from wallet.models import Wallet,Transaction, Userprofile
from django.db import transaction
from datetime import datetime
from django.http import HttpResponseRedirect
from wallet.forms import UserForm, ProfileForm
from django.contrib import messages

# Create your views here.


def add_money(request):
    if request.user:
        if request.POST and request.POST.get('amount'):
            username = request.user.username
            print username
            add_amount = request.POST.get('amount')
            wallet = Wallet.objects.get(username=username)
            wallet.add_money(add_amount)
            wallet.save()
            now = datetime.now()
            trans = Transaction(from_name=username, wallet_id=wallet, date=now, amount=add_amount)
            trans.save()
            return render(request, 'user_profile.html', {'user': request.user,'userprofile': Userprofile.objects.get(user=request.user), 'wallet': wallet})
        else:
            return render(request, 'add_money.html')
    else:
        return HttpResponseRedirect('/login/?next={}'.format('/add_money/'))


def subtract_money(request):
    if request.user:
        if request.POST and request.POST.get('amount'):
            username = request.user.username
            withdraw = request.POST.get('amount')
            wallet = Wallet.objects.get(pk=request.user.userprofile.wallet_id_id)
            if withdraw > wallet.amount:
                return render(request, 'send_money.html', {'error': 'Amount can not be greater than balance'})
            wallet.subtract_money(withdraw)
            wallet.save()
            now = datetime.now()
            trans = Transaction(from_name=username, wallet_id=wallet,to=request.POST.get('receiver-email'), date=now, amount=withdraw)
            trans.save()
            return render(request, 'user_profile.html', {'user': request.user, 'wallet': wallet})
        else:
            return render(request, 'send_money.html')
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
