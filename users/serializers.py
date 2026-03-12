from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile  # Fix: was model = UserSerializer() — must be the model class, not a serializer instance
        fields = ['gender', 'fullname', 'phone', 'image']


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = Profile
        fields = ['fullname', 'username', 'email', 'phone', 'gender', 'image', 'password1', 'password2']

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")

        # Fix: data['username'] is a string, not a queryset — must query the DB to check uniqueness
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already taken")
        return data

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password1')
        validated_data.pop('password2')  # Fix: password2 must be removed before creating Profile

        user = User.objects.create_user(username=username, email=email, password=password)

        profile = Profile.objects.create(
            user=user,
            fullname=validated_data['fullname'],
            phone=validated_data['phone'],
            gender=validated_data['gender'],
            image=validated_data.get('image')
        )
        return profile