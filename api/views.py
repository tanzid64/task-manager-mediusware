from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from .permission import IsAdminOrStaffUser
from task.models import Task
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, TaskCreateSerializer, TaskListSerializer, TaskDetailSerializer, TaskCompleteSerializer

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

# Task App
class TaskListCreateAPIView(generics.ListCreateAPIView):
    
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get_serializer_class(self):
        # Use different serializer classes for listing and creating tasks
        if self.request.method == 'POST':
            return TaskCreateSerializer
        else:
            return TaskListSerializer
    def perform_create(self, serializer):
        # Allow only staff users to create tasks
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise permissions.PermissionDenied("You don't have permission to create tasks.")

class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    lookup_field = 'slug'
    serializer_class = TaskDetailSerializer
    permission_classes = [IsAdminOrStaffUser]

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