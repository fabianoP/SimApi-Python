from rest_framework import serializers
from rest_api.models import Input, Output, User, FmuModelParameters, FileModel


class UserSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = User
        fields = ('user_id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """"""
        user = User(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class FmuModelParametersSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = FmuModelParameters
        fields = ('model_name', 'user', 'idf_file', 'epw_file', 'step_size', 'final_time', 'created_on')

        """read-only field user. Can only be created by authenticated user"""
        extra_kwargs = {'user': {'read_only': True}}


class InputSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Input
        fields = ('user', 'fmu_model', 'created_on', 'time_step', 'yshade')

        """read-only fields user and model_name. Can only be created by authenticated user"""
        extra_kwargs = {'user': {'read_only': True},
                        'fmu_model': {'required': True}}


class OutputSerializer(serializers.ModelSerializer):
    """Outputs received from model time step"""
    class Meta:
        model = Output
        fields = ('user',
                  'fmu_model',
                  'time_step',
                  'yshade',
                  'dry_bulb',
                  'troo',
                  'isolext',
                  'sout',
                  'zonesens',
                  'cool_rate')

        """read-only fields user and model_name. Can only be created by authenticated user"""
        extra_kwargs = {'user': {'read_only': True},
                        'fmu_model': {'read_only': True}}


class UploadSerializer(serializers.ModelSerializer):
    """Test File upload model"""
    class Meta:
        model = FileModel
        fields = ('file',)

