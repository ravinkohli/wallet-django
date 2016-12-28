from rest_framework import serializers
from wallet.models import *


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('username', 'amount', 'id')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {'read_only': True}
        }


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('from_name', 'wallet_id', 'date', 'amount', 'to')
        extra_kwargs = {
            'wallet_id': {'read_only': True},
            'from_name': {'read_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=False)
    class Meta:
        model = Userprofile
        fields = ( 'wallet_id','date_ob', 'sex', 'user')
        extra_kwargs = {
            'wallet_id': {'read_only': True}
        }

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.date_ob = validated_data.get('data_ob', instance.date_ob)
        instance.sex = validated_data.get('sex', instance.sex)
        instance.save()
        return instance
