from django.db.models import fields
from rest_framework.fields import SerializerMethodField
from rest_framework_recursive.fields import RecursiveField
from rest_framework_json_api import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from starrydata.models import Database, Figure, Paper, Tag, Node, Sample, Term

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

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ('name', 'language')

class TagSerializer(serializers.ModelSerializer):
    term_ja = TermSerializer(read_only=True)
    term_ja_id = serializers.PrimaryKeyRelatedField(
        queryset=Term.objects.filter(), source='term_ja', write_only=True, required=False
    )
    term_en = TermSerializer(read_only=True)
    term_en_id = serializers.PrimaryKeyRelatedField(
        queryset=Term.objects.filter(), source='term_ja', write_only=True, required=False
    )
    # TODO: nodesをattributesのままで良いか。言葉の意味的にはrelationshipの方が正しく感じる。
    nodes = NodeSerializer(many=True, required=False)
    included_serializers = {
        'nodes': NodeSerializer,
        'synonyms': TermSerializer
    }
    class Meta:
        model = Tag
        fields = ('term_ja', 'term_en', 'nodes', 'synonyms', 'term_ja_id', 'term_en_id')

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
