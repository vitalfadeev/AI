from rest_framework import serializers
from machine.models import Column

# Serializers define the API representation.
class ColumnSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Column
        fields = ('id', 'column_type', 'name', 'desc',)

