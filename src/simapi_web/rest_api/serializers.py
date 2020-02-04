from rest_framework import serializers
from rest_api.models import Input, Output, Timestep, User, InitModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'name', 'email')


class InitModelSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)

    class Meta:
        model = InitModel
        fields = ('user', 'step_size', 'final_time')


class TimestepSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, required=False)

    class Meta:
        model = Timestep
        fields = ('user', 'time_step')
        # lookup_field = 'user'


class TimestepByUserSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(many=False, required=False)

    class Meta:
        model = Timestep
        fields = ('url', 'user', 'time_step')
        lookup_field = 'user'
        extra_kwargs = {
            'url': {'lookup_field': 'user'},
        }


class InputSerializer(serializers.ModelSerializer):
    time_step = TimestepSerializer(many=False, required=True)

    class Meta:
        model = Input
        fields = ('time_step', 'yshade')


class OutputSerializer(serializers.ModelSerializer):
    time_step = TimestepSerializer(many=False, required=True)

    class Meta:
        model = Output
        fields = ('time_step', 'yshade', 'dry_bulb', 'troo', 'isolext', 'sout', 'zonesens', 'cool_rate')



