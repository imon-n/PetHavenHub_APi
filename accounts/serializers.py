# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserAccount, UserAddress

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['account_no', 'birth_date', 'gender', 'initial_deposite_date', 'balance']

class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ['street_address', 'city', 'postal_code', 'country']

class UserSerializer(serializers.ModelSerializer):
    account = UserAccountSerializer()
    address = UserAddressSerializer()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','password', 'confirm_password', 'account', 'address']

    def create(self, validated_data):
        account_data = validated_data.pop('account')
        address_data = validated_data.pop('address')
        user = User.objects.create(**validated_data)
        UserAccount.objects.create(user=user, **account_data)
        UserAddress.objects.create(user=user, **address_data)
        return user

    def update(self, instance, validated_data):
        account_data = validated_data.pop('account', None)
        address_data = validated_data.pop('address', None)
        user = super().update(instance, validated_data)
        
        if account_data:
            account, created = UserAccount.objects.get_or_create(user=user)
            for attr, value in account_data.items():
                setattr(account, attr, value)
            account.save()

        if address_data:
            address, created = UserAddress.objects.get_or_create(user=user)
            for attr, value in address_data.items():
                setattr(address, attr, value)
            address.save()

        return user



# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, password_validation

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        return user

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError('Old password is not correct')
        password_validation.validate_password(data['new_password'], user)
        return data

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
