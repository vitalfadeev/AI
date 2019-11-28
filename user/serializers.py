from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="myapp:user-detail")

    class Meta:
        model = User
        fields = ('url', 'username')

