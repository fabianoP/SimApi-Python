from rest_framework import serializers
from rest_api.models import Input, Output, User, InitModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        user = User(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class InitModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = InitModel
        fields = ('model_name', 'user', 'step_size', 'final_time', 'created_on')
        extra_kwargs = {'user': {'read_only': True}}


class InputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Input
        fields = ('user', 'model_name', 'time_step', 'yshade')


class OutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Output
        fields = ('user',
                  'model_name',
                  'time_step',
                  'yshade',
                  'dry_bulb',
                  'troo',
                  'isolext',
                  'sout',
                  'zonesens',
                  'cool_rate')



