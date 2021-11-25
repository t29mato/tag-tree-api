from django.db.models import fields
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework_recursive.fields import RecursiveField
from rest_framework_json_api import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from starrydata.models import Tag, Node, Term

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('tag', 'parent')

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ('name', 'language')
        extra_kwargs = {
            'name': {
                'validators': []
            }
        }

class TagSerializer(serializers.ModelSerializer):
    term_ja = TermSerializer(required=False)
    term_ja_id = serializers.PrimaryKeyRelatedField(
        source='term_ja', required=False, read_only=True
    )
    term_en = TermSerializer(required=False)
    term_en_id = serializers.PrimaryKeyRelatedField(
        source='term_en', required=False, read_only=True
    )
    synonyms = TermSerializer(many=True, required=False)
    synonyms_ids = serializers.PrimaryKeyRelatedField(
        source='synonyms', required=False, many=True,read_only=True
    )
    nodes = NodeSerializer(many=True, required=False, read_only=True)
    nodes_ids = serializers.PrimaryKeyRelatedField(
        source='nodes', required=False, many=True, read_only=True
    )

    def create(self, validated_data):
        term_ja_data = validated_data.get('term_ja')
        if term_ja_data:
            term_ja, created = Term.objects.get_or_create(name=term_ja_data['name'])

        term_en_data = validated_data.get('term_en')
        if term_en_data:
            term_en, created = Term.objects.get_or_create(name=term_en_data['name'])

        synonyms = []
        if validated_data.get('synonyms'):
            for term_data in validated_data.get('synonyms'):
                synonym, created = Term.objects.get_or_create(name=term_data['name'])
                synonyms.append(synonym)

        if term_ja_data:
            if term_en_data:
                tag, created = Tag.objects.get_or_create(term_ja=term_ja, term_en=term_en)
            else:
                tag, created = Tag.objects.get_or_create(term_ja=term_ja)
        else:
            if term_en_data:
                tag, created = Tag.objects.get_or_create(term_en=term_en)
            else:
                raise ValueError("タグの用語は日英どちらか１つは必須です。")

        tag.synonyms.set(synonyms)
        return tag

    def update(self, instance, validated_data):
        term_ja_data = validated_data.get('term_ja')
        if term_ja_data:
            term_ja, created = Term.objects.get_or_create(name=term_ja_data['name'], language=term_ja_data['language'])
            instance.term_ja = term_ja

        term_en_data = validated_data.get('term_en')
        if term_en_data:
            term_en, created = Term.objects.get_or_create(name=term_en_data['name'], language=term_en_data['language'])
            instance.term_en = term_en

        synonyms = []
        if validated_data.get('synonyms'):
            for term_data in validated_data.get('synonyms'):
                synonym, created = Term.objects.get_or_create(name=term_data['name'], language=term_data['language'])
                synonyms.append(synonym)
            instance.synonyms.set(synonyms)

        instance.save()
        return instance

    class Meta:
        model = Tag
        fields = ('term_ja', 'term_en', 'nodes', 'synonyms', 'term_ja_id', 'term_en_id', 'synonyms_ids', 'nodes_ids')

class TagTreeSerializer(serializers.Serializer):
    name_ja = serializers.CharField(allow_null=True, allow_blank=True)
    name_en = serializers.CharField(allow_null=True, allow_blank=True)
    node_id = serializers.CharField()
    tag_id = serializers.CharField()
    synonyms_ja = serializers.ListField(child=CharField(), source='synonyms_ja.all')
    synonyms_en = serializers.ListField(child=CharField(), source='synonyms_en.all')
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
