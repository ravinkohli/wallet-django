from django.db import models  # , connection
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from rest_framework.authtoken.models import Token

def validate_not_neg(value):
    if value < 0:
        raise ValidationError(
            ('%s cannot be negative' % value),
            params={'value': value}
        )


class Wallet(models.Model):
    username = models.CharField(max_length=15,default='')
    amount = models.IntegerField(validators=[validate_not_neg], default=0)

    def add_money(self, money):
        self.amount += int(money)
        self.save()

    def subtract_money(self, money):
        self.amount -= int(money)
        self.save()

    def __str__(self):
        return self.username

    class Meta:
        permissions = (('add_money', 'can deposit money'), ('subtract_money', 'can take withdraw money'))


class Transaction(models.Model):
    from_name = models.CharField(max_length=15)
    wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.IntegerField()
    to = models.EmailField(null=True, blank=True)
    def __str__(self):
        return self.id


class Userprofile(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    date_ob = models.DateField(null=True, blank=True)
    sex = models.CharField(max_length=1, null=True)

    def __str__(self):
        return str(self.user)



    # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Userprofile.objects.create(user=instance)
    #
    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()
