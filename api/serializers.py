from rest_framework import serializers
from django.contrib.auth import get_user_model
# Models
from account.models import User
from task.models import Task, Photo

# Account App
class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'gender', 'password', 'confirm_password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']