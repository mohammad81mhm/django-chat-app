from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers
from .models import User, OTP
import re


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=11,
        min_length=11,
        validators=[
            MaxLengthValidator(11),
        ]
    )

    def validate_phone_number(self, value):
        if not re.match(r'^\d{11}$', value):
            raise serializers.ValidationError("Phone number must be 11 digits.")
        return value


class OTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'profile_picture' , 'username']

    def update(self, instance, validated_data):
        profile_picture = validated_data.get('profile_picture', None)
        if profile_picture:
            instance.profile_picture = profile_picture

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.username = validated_data.get('username', instance.username)

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'username', 'first_name', 'last_name', 'profile_picture']