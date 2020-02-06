from rest_framework import serializers
from . import models

# /user/id/init_model
# should store the init params in db and call method to pass json to simulation container
# POST, GET

# /user/id/input
# should store input in db and pass to sim container
# POST, GET

# /user/id/ouput
# should retrieve from container and store in db
# POST, GET

# Implement data/time and random name for each simulation ran. Send user email with all settings for the simulation
# just ran or text file with same


class InitModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InitModel
        fields = ['model_name', 'step_size', 'final_time']


class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Input
        fields = ['time_step', 'yshade']


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Output
        fields = ('time_step', 'yshade', 'dry_bulb', 'troo', 'isolext', 'sout', 'zonesens', 'cool_rate')


class UserSerializer(serializers.ModelSerializer):
    init_model = InitModelSerializer(many=False, allow_null=True)
    input = InputSerializer(many=False, allow_null=True, required=False, read_only=True)
    output = OutputSerializer(many=False, allow_null=True, required=False, read_only=True)

    class Meta:
        model = models.User
        fields = ['user_id', 'email', 'name', 'init_model', 'input', 'output']

