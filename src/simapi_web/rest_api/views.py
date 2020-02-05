from rest_framework import renderers
from rest_framework.response import Response
import rest_framework.generics
from rest_framework.decorators import action
from rest_framework import status, viewsets
from .models import User, InitModel
from . import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer




"""
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    @action(detail=True, methods=['post'])
    def init_model(self, request, pk=None):
        user = self.get_object()
        serializer = serializers.InitModelSerializerDetail(data=request.data)
        if serializer.is_valid():
            model_params = InitModel(user=user,
                                     step_size=serializer.data['step_size'],
                                     final_time=serializer.data['final_time'])
            model_params.save()
            return Response({'status': 'success'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
"""



