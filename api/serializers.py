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

class UserProfileSerializer(serializers.ModelSerializer):
    task_history_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'task_history_count']
    def get_task_history_count(self, obj):
        return Task.objects.filter(completed_by=obj).count()

# Task
class TaskCreateSerializer(serializers.ModelSerializer):
    task_photo = serializers.ImageField(required=False)
    class Meta:
        model = Task
        exclude = ['is_completed', 'completed_by', 'slug']
    def create(self, validated_data):
        task_photo_data = validated_data.pop('task_photo', None)

        task = super().create(validated_data)

        if task_photo_data:
            Photo.objects.create(task=task, **task_photo_data)

        return task

class TaskListSerializer(serializers.ModelSerializer):
    task_photo = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = '__all__'
    def get_task_photo(self, obj):
        photos = Photo.objects.filter(task=obj)
        try:
            serialized_photos = [{'image': photo.image.url} for photo in photos]
        except:
            serialized_photos = "No Photos"
        return serialized_photos

class TaskDetailSerializer(serializers.ModelSerializer):
    task_photo = serializers.ImageField(required=False)
    class Meta:
        model = Task
        fields = "__all__"
    def get_task_photo(self, obj):
        photos = Photo.objects.filter(task=obj)
        try:
            serialized_photos = [{'image': photo.image.url} for photo in photos]
        except:
            serialized_photos = "No Photos"
        return serialized_photos
    
class TaskCompleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_completed']
