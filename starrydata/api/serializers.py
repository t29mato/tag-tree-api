from django.db.models import fields
from rest_framework_json_api import serializers
from starrydata.models import FabricationProcess, SynthesisMethodTag, SynthesisMethodTagTreeNode


class FabricationProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = FabricationProcess
        fields = '__all__'

class SynthesisMethodTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynthesisMethodTag
        fields = '__all__'

class SynthesisMethodTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynthesisMethodTag
        fields = '__all__'

class SynthesisMethodTagTreeNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SynthesisMethodTagTreeNode
        fields = '__all__'
