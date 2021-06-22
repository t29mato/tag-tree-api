from django.db.models import fields
from rest_framework import serializers
from starrydata.models import FabricationProcess


class FabricationProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricationProcess
        fields = '__all__'
