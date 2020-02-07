from rest_framework import viewsets
from .models import User
from .serializers import UserInitSerializer, UserSerializer, UserInputSerializer, UserOutputSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserInitViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInitSerializer


class UserInputViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInputSerializer


class UserOutputViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserOutputSerializer



