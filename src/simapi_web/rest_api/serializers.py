from rest_framework import serializers
from .models import InitModel, Input, Output, User


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
        model = InitModel
        fields = ['model_id', 'model_name', 'step_size', 'final_time']


class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        fields = ['time_step', 'yshade']


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = ('time_step', 'yshade', 'dry_bulb', 'troo', 'isolext', 'sout', 'zonesens', 'cool_rate')


class UserSerializer(serializers.ModelSerializer):
    init_model = InitModelSerializer(read_only=True)  # InitModelSerializer(many=False, allow_null=True)
    input = InputSerializer(read_only=True)
    output = OutputSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'email', 'name', 'init_model', 'input', 'output']


class UserInitSerializer(serializers.ModelSerializer):
    init_model = InitModelSerializer(many=False)  # InitModelSerializer(many=False, allow_null=True)
    input = InputSerializer(read_only=True, allow_null=True, required=False)
    output = OutputSerializer(read_only=True, allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['user_id', 'email', 'name', 'init_model', 'input', 'output']

    def update(self, instance, validated_data):
        model_data = validated_data.pop('init_model')

        instance.init_model = InitModel(model_name=model_data.get('model_name'),
                                        step_size=model_data.get('step_size'),
                                        final_time=model_data.get('final_time'))
        instance.init_model.save()
        instance.save()
        return instance


class UserInputSerializer(serializers.ModelSerializer):
    init_model = InitModelSerializer(read_only=True, allow_null=True, required=False)
    input = InputSerializer(many=False)
    output = OutputSerializer(read_only=True, allow_null=True, required=False)

    class Meta:
        model = User
        fields = ['user_id', 'email', 'name', 'init_model', 'input', 'output']

    def update(self, instance, validated_data):
        model_data = validated_data.pop('input')
        instance.input = Input(time_step=model_data.get('time_step'),
                               yshade=model_data.get('yshade'))
        instance.input.save()
        instance.save()
        return instance


class UserOutputSerializer(serializers.ModelSerializer):
    init_model = InitModelSerializer(read_only=True, allow_null=True, required=False)
    input = InputSerializer(read_only=True, allow_null=True, required=False)
    output = OutputSerializer(many=False)

    class Meta:
        model = User
        fields = ['user_id', 'email', 'name', 'init_model', 'input', 'output']

    def update(self, instance, validated_data):
        model_data = validated_data.pop('output')

        instance.output = Output(time_step=model_data.get('time_step'),
                                 yshade=model_data.get('yshade'),
                                 dry_bulb=model_data.get('dry_bulb'),
                                 troo=model_data.get('troo'),
                                 isolext=model_data.get('isolext'),
                                 sout='sout',
                                 zonesens=model_data.get('zonesens'),
                                 cool_rate='cool_rate')

        instance.output.save()
        instance.save()
        return instance
