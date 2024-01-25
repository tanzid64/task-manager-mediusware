from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from .permission import IsAdminOrStaffUser
from django.contrib.auth.views import PasswordResetView
from task.models import Task
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, TaskCreateSerializer, TaskListSerializer, TaskDetailSerializer, TaskCompleteSerializer, PasswordChangeSerializer, PasswordResetSerializer
from rest_framework import viewsets
from .filters import TaskFilter
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import filters
# Account App
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response({'detail': 'User creation successful.'}, status=status.HTTP_201_CREATED, headers=headers) 
    
class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)

class UserLogoutAPIView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login-api')
    
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserPasswordChangeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetAPIView(APIView, PasswordResetView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return self.form_valid(serializer)
        return self.form_invalid(serializer)
    
# Task App
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()    
    # filter 
    filter_backends = [ DjangoFilterBackend]
    filterset_class = TaskFilter
    def get_serializer_class(self):
        # Use different serializer classes for listing and creating tasks
        if self.request.method == 'POST':
            return TaskCreateSerializer
        else:
            return TaskListSerializer
    def create(self, request, *args, **kwargs):
        # Check if the user is an admin before allowing task creation
        if not request.user.is_staff:
            return Response({"detail": "Permission denied. Only admins can create tasks."}, status=status.HTTP_403_FORBIDDEN)
    def update(self, request, *args, **kwargs):
        # Check if the user is an admin before allowing task creation
        if not request.user.is_staff:
            return Response({"detail": "Permission denied. Only admins can create tasks."}, status=status.HTTP_403_FORBIDDEN)
    def partial_update(self, request, *args, **kwargs):
        # Check if the user is an admin before allowing task creation
        if not request.user.is_staff:
            return Response({"detail": "Permission denied. Only admins can create tasks."}, status=status.HTTP_403_FORBIDDEN)
    def destroy(self, request, *args, **kwargs):
        # Check if the user is an admin before allowing task creation
        if not request.user.is_staff:
            return Response({"detail": "Permission denied. Only admins can create tasks."}, status=status.HTTP_403_FORBIDDEN)


class TaskCompleteAPIView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCompleteSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticated]
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(is_completed=True, completed_by=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)