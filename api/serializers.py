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


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        request = self.context.get('request')
        user = request.user

        # Validate old password
        old_password = data.get('old_password')
        if not user.check_password(old_password):
            raise serializers.ValidationError("Invalid old password.")

        # Validate new passwords match
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')
        if new_password1 != new_password2:
            raise serializers.ValidationError("New passwords do not match.")

        return data

    def save(self, **kwargs):
        request = self.context.get('request')
        user = request.user

        # Save new password
        new_password = self.validated_data['new_password1']
        user.set_password(new_password)
        user.save()

        # You can perform additional actions here, e.g., logging the change
        return user

# Task
    
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['image']

class TaskCreateSerializer(serializers.ModelSerializer):
    task_photos = PhotoSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Task
        exclude = ['is_completed', 'completed_by', 'slug']

    def create(self, validated_data):
        task_photos_data = validated_data.pop('task_photos', None)

        task = super().create(validated_data)

        if task_photos_data:
            for photo_data in task_photos_data:
                Photo.objects.create(task=task, **photo_data)

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
