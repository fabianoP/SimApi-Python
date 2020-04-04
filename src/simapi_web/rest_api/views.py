import json

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.db import transaction
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_api import serializers
from rest_api import models
from rest_api import tasks


class UserViewSet(viewsets.ModelViewSet):
    """retrieve list of or create new user"""

    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    authentication_classes = (TokenAuthentication,)


class LoginViewSet(viewsets.ViewSet):
    """checks email and password and returns an auth token"""

    serializer_class = AuthTokenSerializer

    @staticmethod
    def create(request):
        return ObtainAuthToken().post(request)


class FmuModelViewSet(viewsets.ModelViewSet):
    """handles creating and reading model initialization parameters"""

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = serializers.FmuModelParametersSerializer
    queryset = models.FmuModel.objects.all()

    def perform_create(self, serializer):

        if self.request.POST.get('container_id') is None:
            self.request.data['container_id'] = 'src_simulator_1'

        serializer.save(user=self.request.user, container_id=self.request.data['container_id'])

        data = {'model_name': self.request.data['model_name'],
                'step_size': self.request.data['step_size'],
                'final_time': self.request.data['final_time'],
                'container_id': self.request.data['container_id'],
                'Authorization': 'Token ' + str(self.request.auth)
                }

        if self.request.data['container_id'] not in self.request.data['model_name']:
            transaction.on_commit(lambda: tasks.post_model.apply_async((data,), queue='web', routing_key='web'))


class InputViewSet(viewsets.ModelViewSet):
    """handles creating and reading model input parameters"""

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = serializers.InputSerializer
    queryset = models.Input.objects.all()

    """
    create new input instance. set user as current authenticated user,
    fmu_model as current fmu_model related to user
    """

    def perform_create(self, serializer, **kwargs):
        # TODO add second get param of time/date to ensure the current model is returned
        model = models.FmuModel.objects.get(model_name=self.request.data['fmu_model'])

        input_json_field = self.request.data['input_json']
        time_step = self.request.data['time_step']

        data = {
            'time_step': time_step,
            'container_id': model.container_id
        }

        serializer.save(user=self.request.user, fmu_model=model, time_step=time_step, input_json=input_json_field)

        transaction.on_commit(lambda: tasks.post_input.apply_async((data,),
                                                                   queue='web',
                                                                   routing_key='web'))


class OutputViewSet(viewsets.ModelViewSet):
    """handles creating and reading model output parameters"""

    authentication_classes = (TokenAuthentication, SessionAuthentication)
    serializer_class = serializers.OutputSerializer
    queryset = models.Output.objects.all()

    """
    create new output instance. set user as current authenticated user,
    fmu_model as current init_model related to user
    """

    def perform_create(self, serializer, **kwargs):
        # TODO add second get param of time/date to ensure the current model is returned
        output = self.request.data
        model = models.FmuModel.objects.get(model_name=output['fmu_model'])
        output_json_field = output['output_json']
        time_step = output['time_step']
        serializer.save(user=self.request.user, fmu_model=model, time_step=time_step,
                        output_json=json.dumps(output_json_field))


class HostNameViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.HostNameSerializer
    queryset = models.ContainerHostNames.objects.all()

    def perform_create(self, serializer):
        serializer.save(hostname=self.request.data['hostname'])
