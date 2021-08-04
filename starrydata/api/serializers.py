from django.db.models import fields
from rest_framework.fields import SerializerMethodField
from rest_framework_recursive.fields import RecursiveField
from rest_framework_json_api import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from starrydata.models import Database, Figure, Paper, Tag, Node, Sample, Word

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

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('tag', 'parent')

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ('name', 'language')

class TagSerializer(serializers.ModelSerializer):
    included_serializers = {
        'nodes': NodeSerializer,
        'word_ja': WordSerializer,
        'word_en': WordSerializer,
        'synonym': WordSerializer
    }
    class Meta:
        model = Tag
        fields = ('word_ja', 'word_en', 'nodes', 'synonym')

class TagTreeSerializer(serializers.Serializer):
    name_ja = serializers.CharField(allow_null=True, allow_blank=True)
    name_en = serializers.CharField(allow_null=True, allow_blank=True)
    node_id = serializers.CharField()
    tag_id = serializers.CharField()
    parent_node_id = serializers.CharField(allow_null=True, required=False)
    tree_level = serializers.IntegerField()
    children = serializers.ListField(child=RecursiveField(), source='children.all')

class TagAncestorSerializer(serializers.Serializer):
    name_ja = serializers.CharField(allow_null=True, allow_blank=True)
    name_en = serializers.CharField(allow_null=True, allow_blank=True)
    node_id = serializers.CharField()
    tag_id = serializers.CharField()
    parent_node_id = serializers.CharField(allow_null=True, required=False)

class TagAncestorListSerializer(serializers.Serializer):
    ancestors = serializers.ListField(child=TagAncestorSerializer(), source='ancestors.all')
