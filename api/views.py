from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer

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


