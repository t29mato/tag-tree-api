from django.db.models import fields
from rest_framework.fields import SerializerMethodField
from rest_framework_recursive.fields import RecursiveField
from rest_framework_json_api import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from starrydata.models import Database, FabricationProcess, Figure, Paper, PolymerTag, PolymerTagTreeNode, Sample, SynthesisMethodTag, SynthesisMethodTagTreeNode

class DatabaseSerializer(serializers.ModelSerializer, SerializerExtensionsMixin):
    paper_count = SerializerMethodField()
    figure_count = SerializerMethodField()
    sample_count = SerializerMethodField()
    class Meta:
        model = Database
        fields = '__all__'

    def get_paper_count(self, obj):
        return len(Paper.objects.all().filter(database = obj.id))

    def get_figure_count(self, obj):
        return len(Figure.objects.all().filter(paper__database = obj.id))

    def get_sample_count(self, obj):
        return len(Sample.objects.all().filter(paper__database = obj.id))

class PaperSerializer(serializers.ModelSerializer):
    figure_count = SerializerMethodField()
    sample_count = SerializerMethodField()

    class Meta:
        model = Paper
        fields = '__all__'

    def get_figure_count(self, obj):
        return len(Figure.objects.all().filter(paper__database = obj.id))

    def get_sample_count(self, obj):
        return len(Sample.objects.all().filter(paper__database = obj.id))

class FigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Figure
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = '__all__'

class PolymerTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolymerTag
        fields = '__all__'

class PolymerTagTreeSerializer(serializers.Serializer):
    name = serializers.CharField()
    children = serializers.ListField(child=RecursiveField(), source='children.all')

class PolymerTagTreeChildNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolymerTagTreeNode
        fields = '__all__'

class PolymerTagTreeNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolymerTagTreeNode
        fields = '__all__'

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
