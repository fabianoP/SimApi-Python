from rest_framework import viewsets
from rest_api.serializers import UserSerializer, InitModelSerializer
from rest_framework.decorators import action
from rest_api.models import User, InitModel

from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from . import permissions
# Create your views here.
# TODO  figure out mod headers to use login token, and test InitModel.
# implement rest of the viewsets, add class filters to return all instances associated with user
# Possibly have master script in while(time < final_time) and have the pauses inside the loop.
# comment code,


class UserViewSet(viewsets.ModelViewSet):
    """retrieve list of or create new user"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)


class LoginViewSet(viewsets.ViewSet):
    """checks email and password and returns an auth token"""

    serializer_class = AuthTokenSerializer

    @staticmethod
    def create(request):

        return ObtainAuthToken().post(request)


class InitModelViewSet(viewsets.ModelViewSet):
    """Handles creating and reading model initialization parameters"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = InitModelSerializer
    queryset = InitModel.objects.all()

    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
