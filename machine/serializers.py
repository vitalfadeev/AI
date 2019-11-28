from rest_framework import serializers
from machine.models import Machine


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ("__all__")
        depth = 1

    # Owner_User_ID = serializers.ReadOnlyField( source='owner.username' )

    # def validate(self, attrs):
    #     return attrs


    # def create(self, validated_data):
    #     instance = super().create( validated_data )
    #
    #     if instance:
    #         from machine.loader import django_loader
    #
    #         url = instance.input_file.path
    #         django_loader.prenanlyze_and_load( url, instance )
    #
    #     return instance


    # def save(self, **kwargs):
    #     return self.instance

