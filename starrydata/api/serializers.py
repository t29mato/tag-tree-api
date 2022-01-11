from typing import Optional, TypedDict
from rest_framework.fields import CharField
from rest_framework_recursive.fields import RecursiveField
from rest_framework_json_api import serializers
from starrydata.models import Tag, Node, TagTree

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ('tag', 'parent')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'memo')

class TagTreeListSerializer(serializers.Serializer):
    name = serializers.CharField()
    key = serializers.CharField()

    def create(self, validated_data):
        return TagTree.objects.create(**validated_data)

class TagTreeSerializer(serializers.Serializer):
    tag_name = serializers.CharField()
    tree_level = serializers.IntegerField(required=False)
    children = serializers.ListField(child=RecursiveField(), source='children.all')

class TagTreeDetailSerializer(serializers.Serializer):
    Tree = TypedDict('Tree', {'tag_name': str, 'node_id': str, 'tag_id': str, 'tree_level': int, 'children': Optional[list['Tree']]})
    name = serializers.CharField()
    key = serializers.CharField()
    tree = TagTreeSerializer(allow_null=True)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.key = validated_data.get('key', instance.key)
        root_tag = Tag.objects.get_or_create(name=self.data.get('tree')['tag_name'])[0]
        root_node, created = Node.objects.get_or_create(
            tag=root_tag,
            )
        instance.node = root_node
        instance.save()
        Node.objects.filter(parent=root_node.id).delete()
        list(map(lambda child: self.__saveTree(child, root_node.id), self.data.get('tree')['children']))
        return instance


    def __saveTree(self, data: Tree, parent_id: str):
        tag, created = Tag.objects.get_or_create(name=data['tag_name'])
        node, created = Node.objects.get_or_create(tag=tag, parent_id=parent_id)
        list(map(lambda child: self.__saveTree(child, node.id), data['children']))





