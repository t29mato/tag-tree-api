from typing import List, Optional, TypedDict
from rest_framework import generics, serializers, views, permissions
from rest_framework.response import Response
from django.db.models import F
from django.http import Http404
from starrydata.models import Tag, Node, TagTree
from starrydata.api.serializers import TagSerializer, NodeSerializer, TagTreeDetailSerializer, TagTreeListSerializer, TagTreeSerializer

class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
    search_fields = ['name']
    def get_permissions(self):
        self.permission_classes = {
            'POST': [permissions.IsAuthenticated]
        }.get(self.request.method, [])
        return super(TagListView, self).get_permissions()

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer
    def get_permissions(self):
        self.permission_classes = {
            'POST': [permissions.IsAuthenticated],
            'PUT': [permissions.IsAuthenticated],
            'PATCH': [permissions.IsAuthenticated],
            'DELETE': [permissions.IsAuthenticated]
        }.get(self.request.method, [])
        return super(TagDetailView, self).get_permissions()

class NodeListView(generics.ListCreateAPIView):
    queryset = Node.objects.select_related('tag', 'parent').all().order_by('id')
    serializer_class = NodeSerializer
    def get_permissions(self):
        self.permission_classes = {
            'POST': [permissions.IsAuthenticated]
        }.get(self.request.method, [])
        return super(TagListView, self).get_permissions()

class NodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.select_related('tag', 'parent').all().order_by('id')
    serializer_class = NodeSerializer
    def get_permissions(self):
        self.permission_classes = {
            'POST': [permissions.IsAuthenticated],
            'PUT': [permissions.IsAuthenticated],
            'PATCH': [permissions.IsAuthenticated],
            'DELETE': [permissions.IsAuthenticated]
        }.get(self.request.method, [])
        return super(TagDetailView, self).get_permissions()

class TagTreeListView(views.APIView):
    # to generate API docs
    def get_serializer(self):
        return TagTreeListSerializer

    def get_permissions(self):
        self.permission_classes = {
            # 'POST': [permissions.IsAuthenticated],
        }.get(self.request.method, [])
        return super(TagTreeListView, self).get_permissions()

    def get(self, request):
        serializer = TagTreeListSerializer(TagTree.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TagTreeListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response(data=serializer.data, status=201)


class TagTreeDetailView(views.APIView):
    Tree = TypedDict('Tree', {'tag_name': str, 'node_id': str, 'tag_id': str, 'tree_level': int, 'children': Optional[list['Tree']]})
    Node = TypedDict('Tree', {'tag_name': str, 'node_id': str, 'tag_id': str, 'parent_node_id': str})
    # to generate API docs
    def get_serializer(self):
        return TagTreeDetailSerializer

    def get(self, request, pk):
        tag_tree = TagTree.objects.get(pk=pk)
        data = {
            'name': tag_tree.name,
            'key': tag_tree.key,
            'id': pk,
            'tree': None,
        }
        if tag_tree.node is None:
            serializer = TagTreeDetailSerializer(
                data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=200)

        nodes = list(Node.objects.all().annotate(
            tag_name=F('tag__name'),
            node_id=F('id'),
            parent_node_id=F('parent_id')
            ).values('node_id','parent_node_id', 'tag_id', 'tag_name'))
        root = Node.objects.annotate(
            tag_name=F('tag__name'),
            node_id=F('id'),
            ).values('node_id', 'tag_id', 'tag_name').get(pk=tag_tree.node.id)
        data['tree'] = self.__generateTree(root, nodes, 0)
        serializer = TagTreeDetailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=200)

    def __generateTree(self, parent: Tree, nodes: List[Node], tree_level: int):
        # if tree_level == 1:
        #     return parent
        children = list(filter(lambda node: node['parent_node_id'] == parent['node_id'], nodes))
        parent['tree_level'] = tree_level
        tree_level = tree_level + 1
        parent['children'] = list(map(lambda child: self.__generateTree(child, nodes, tree_level), children))
        return parent

    def patch(self, request, pk, *args, **kwargs):
        serializer = TagTreeDetailSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(
            instance=TagTree.objects.get(pk=pk),
            validated_data=serializer.validated_data)
        return Response(serializer.data, status=200)
