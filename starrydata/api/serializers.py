from django.db.models import fields
from rest_framework.fields import SerializerMethodField
from rest_framework_json_api import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from starrydata.models import Database, FabricationProcess, Figure, Paper, Sample, SynthesisMethodTag, SynthesisMethodTagTreeNode

class DatabaseSerializer(serializers.ModelSerializer, SerializerExtensionsMixin):
    paper_count = SerializerMethodField()
    figure_count = SerializerMethodField()
    sample_count = SerializerMethodField()
    class Meta:
        model = Database
        fields = [
            'id',
            'name',
            'paper_count',
            'figure_count',
            'sample_count',
        ]

    def get_paper_count(self, obj):
        return len(Paper.objects.all().filter(database = obj.id))

    def get_figure_count(self, obj):
        return len(Figure.objects.all().filter(paper__database = obj.id))

    def get_sample_count(self, obj):
        return len(Sample.objects.all().filter(paper__database = obj.id))

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = '__all__'
class FigureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Figure
        fields = '__all__'

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
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
