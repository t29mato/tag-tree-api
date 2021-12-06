from django.db.models import fields
from rest_framework.fields import CharField, SerializerMethodField
from rest_framework_recursive.fields import RecursiveField
from rest_framework_json_api import serializers
from rest_framework_serializer_extensions.serializers import SerializerExtensionsMixin
from starrydata.models import Tag, Node, TagMemo

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('tag', 'parent')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)

class TagMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagMemo
        fields = ('tag', 'memo')

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
