from rest_framework.fields import CharField
from rest_framework_recursive.fields import RecursiveField
from rest_framework_json_api import serializers
from starrydata.models import Tag, Node

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('tag', 'parent')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'memo')

class TagTreeSerializer(serializers.Serializer):
    name = serializers.CharField()
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
