from rest_framework import serializers
from wallet.models import *


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('username', 'amount')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('from_name', 'wallet_id', 'date', 'amount', 'to')
