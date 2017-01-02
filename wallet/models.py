from django.db import models  # , connection
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# Create your models here.
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
from rest_framework_expiring_authtoken.models import ExpiringToken
import binascii
import os
from django.utils import timezone
from rest_framework_expiring_authtoken.settings import token_settings
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
import datetime

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


@python_2_unicode_compatible
class DeviceToken(models.Model):
    """
    The default authorization token model.
    """
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(User, related_name='%(class)s_auth_token',
                             on_delete=models.CASCADE,)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    device_browser = models.CharField(max_length=25, null=True)
    is_active = models.BooleanField(default=False)
    expired_date = models.DateField(blank=True, null=True)

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        if not self.expired_date:
            self.expired_date = self.created.date() + token_settings.EXPIRING_TOKEN_LIFESPAN
        return super(DeviceToken, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

    def expired(self):
        """Return boolean indicating token expiration."""
        if self.is_active:
            now = timezone.now()
            if self.created < now - token_settings.EXPIRING_TOKEN_LIFESPAN:
                return True
        return False
