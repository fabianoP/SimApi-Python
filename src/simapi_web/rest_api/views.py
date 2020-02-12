from rest_framework import viewsets
from rest_api import serializers
from rest_framework.decorators import action
from rest_api import models

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from . import permissions
# Create your views here.
# TODO  re-work model foreign key. if user has more than one model api breaks.
# Possibly have master script in while(time < final_time) and have the pauses inside the loop.


class UserViewSet(viewsets.ModelViewSet):
    """retrieve list of or create new user"""

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    authentication_classes = (TokenAuthentication,)
    # permission_classes = (permissions.UpdateOwnProfile,)


class LoginViewSet(viewsets.ViewSet):
    """checks email and password and returns an auth token"""

    serializer_class = AuthTokenSerializer

    @staticmethod
    def create(request):

        return ObtainAuthToken().post(request)


class InitModelViewSet(viewsets.ModelViewSet):
    """handles creating and reading model initialization parameters"""

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = serializers.InitModelSerializer
    queryset = models.InitModel.objects.all()

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)


class InputViewSet(viewsets.ModelViewSet):
    """handles creating and reading model input parameters"""

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = serializers.InputSerializer
    queryset = models.Input.objects.all()

    """create new input instance. set user as current authenticated user, model_name as init_model related to user"""
    def perform_create(self, serializer):

        model = models.InitModel.objects.get(user=self.request.user)
        serializer.save(user=self.request.user, model_name=model)


class OutputViewSet(viewsets.ModelViewSet):
    """handles creating and reading model output parameters"""

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = serializers.OutputSerializer
    queryset = models.Output.objects.all()

    """create new output instance. set user as current authenticated user, model_name as init_model related to user"""
    def perform_create(self, serializer):

        model = models.InitModel.objects.get(user=self.request.user)
        serializer.save(user=self.request.user, model_name=model)
