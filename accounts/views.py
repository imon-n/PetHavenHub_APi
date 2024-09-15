from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from .models import UserAccount, UserAddress
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .serializers import LoginSerializer, PasswordChangeSerializer, UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny] 

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response({'detail': 'Login successful'})

class LogoutView(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]
    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response({'detail': 'Logout successful'})

class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny] 

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Password changed successfully'})