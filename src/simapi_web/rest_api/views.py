from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_api.serializers import UserSerializer, TimestepSerializer, InputSerializer, OutputSerializer, \
    InitModelSerializer, TimestepByUserSerializer

from rest_api.models import Input, User, Output, Timestep, InitModel


# Create your views here.


class ListUserView(ListCreateAPIView):
    """
    API view to retrieve list of or create new time step
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class DetailsUserView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ListInitModelView(ListCreateAPIView):
    """
    API view to retrieve list of or create new time step
    """

    serializer_class = InitModelSerializer
    queryset = InitModel.objects.all()


class DetailsInitModelView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """

    serializer_class = InitModelSerializer
    queryset = InitModel.objects.all()


class ListTimestepView(ListCreateAPIView):
    """
    API view to retrieve list of or create new time step
    """

    serializer_class = TimestepSerializer
    queryset = Timestep.objects.all()


class DetailsTimestepView(viewsets.ModelViewSet):
    """
    API view to retrieve, update or delete post
    """
    queryset = Timestep.objects.all()
    serializer_class = TimestepByUserSerializer
    lookup_field = 'user'
    # user_id =

    def get_queryset(self):
        qs = Timestep.objects.all()
        filtered = qs.filter(user_id=self.kwargs.get('user'))
        return filtered


class ListInputView(ListCreateAPIView):
    """
    API view to retrieve list of or create new input
    """

    serializer_class = InputSerializer
    queryset = Input.objects.all()


class DetailsInputView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = InputSerializer
    queryset = Input.objects.all()


class ListOutputView(ListCreateAPIView):
    """
    API view to retrieve list of or create new output
    """

    serializer_class = OutputSerializer
    queryset = Output.objects.all()


class DetailsOutputView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete post
    """
    serializer_class = OutputSerializer
    queryset = Output.objects.all()
