from rest_framework import serializers
from machine.models import Machine


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ("__all__")
        depth = 1


class MachineInputLinesSerializer(serializers.Serializer):
    my_field = None
