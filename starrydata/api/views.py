from typing import List, Optional, TypedDict
from rest_framework import generics, views, permissions
from rest_framework.response import Response
from django.db.models import F
from django.http import Http404
from starrydata.models import Tag, Node, TagTree
from starrydata.api.serializers import TagAncestorListSerializer, TagSerializer, NodeSerializer, TagTreeListSerializer, TagTreeSerializer

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

class TagTreeListView(generics.ListCreateAPIView):
    queryset = TagTree.objects.all().order_by('id')
    serializer_class = TagTreeListSerializer

class TagTreeDetailView(views.APIView):
    Tree = TypedDict('Tree', {'name': str, 'node_id': str, 'tag_id': str, 'tree_level': int, 'children': Optional[list['Tree']]})
    Node = TypedDict('Tree', {'name': str, 'node_id': str, 'tag_id': str, 'parent_node_id': str})
    def get(self, request, pk):
        nodes = list(Node.objects.all().annotate(
            name=F('tag__name'),
            node_id=F('id'),
            parent_node_id=F('parent_id')
            ).values('node_id','parent_node_id', 'tag_id', 'name'))
        try:
            root = Node.objects.annotate(
                name=F('tag__name'),
                node_id=F('id'),
                ).values('node_id', 'tag_id', 'name').get(pk=pk)
        except Node.DoesNotExist:
            raise Http404

        tree = self.__generateTree(root, nodes, 0)
        serializer = TagTreeSerializer(data=tree)
        try:
            if not serializer.is_valid():
                raise ValueError("シリアライズのバリデーションに失敗", serializer.errors)
        except ValueError as e:
            print(e)
            print('バリデーション失敗')
        return Response(serializer.data, status=200)

    def __generateTree(self, parent: Tree, nodes: List[Node], tree_level: int):
        # if tree_level == 1:
        #     return parent
        tree_level = tree_level + 1
        children = list(filter(lambda node: node['parent_node_id'] == parent['node_id'], nodes))
        parent['tree_level'] = tree_level
        parent['children'] = list(map(lambda child: self.__generateTree(child, nodes, tree_level), children))
        return parent

class TagAncestorsView(views.APIView):
    Node = TypedDict('Node', {'name_ja': str, 'name_en': str, 'node_id': str, 'tag_id': str, 'parent_node_id': str})

    def get(self, request, pk):
        ancestors = self.__generateAncestors(pk, [])
        serializer = TagAncestorListSerializer(data=ancestors)
        try:
            if not serializer.is_valid():
                raise ValueError("シリアライズのバリデーションに失敗", serializer.errors)
        except ValueError as e:
            print(e)
            print('バリデーション失敗')
        print(serializer.data)
        return Response(data=serializer.data, status=200)

    def __generateAncestors(self, parent_id: int, ancestors: List[Node] = []):
        if not parent_id:
            return {"ancestors": ancestors}
        else:
            node = Node.objects.filter(pk=parent_id).annotate(
                name_ja=F('tag__term_ja__name'),
                name_en=F('tag__term_en__name'),
                node_id=F('id'),
                parent_node_id=F('parent_id')
                ).values('node_id','parent_node_id', 'tag_id', 'name_ja', 'name_en')[0]
            ancestors.append(node)
            return self.__generateAncestors(node['parent_node_id'], ancestors)
