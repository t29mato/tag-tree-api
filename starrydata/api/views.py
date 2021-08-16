from typing import List, Optional, TypedDict
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from django.db.models import F
from django.http import Http404
from starrydata.models import Database, Figure, Paper, Tag, Node, Sample, Term
from starrydata.api.serializers import DatabaseSerializer, FigureSerializer, PaperSerializer, TagAncestorListSerializer, TagAncestorSerializer, TagSerializer, NodeSerializer, SampleSerializer, TagTreeSerializer, TermSerializer

class DatabaseListView(generics.ListCreateAPIView):
    queryset = Database.objects.all().order_by('id')
    serializer_class = DatabaseSerializer

class PaperListView(generics.ListCreateAPIView):
    queryset = Paper.objects.all().order_by('id')
    serializer_class = PaperSerializer

class FigureListView(generics.ListCreateAPIView):
    queryset = Figure.objects.all().order_by('id')
    serializer_class = FigureSerializer

class SampleListView(generics.ListCreateAPIView):
    queryset = Sample.objects.all().order_by('id')
    serializer_class = SampleSerializer


class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.select_related('term_ja', 'term_en').prefetch_related('synonyms', 'nodes').all().order_by('id')
    serializer_class = TagSerializer
    search_fields = ['term_ja__name', 'term_en__name']

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.select_related('term_ja', 'term_en').prefetch_related('synonyms', 'nodes').all().order_by('id')
    serializer_class = TagSerializer

class NodeListView(generics.ListCreateAPIView):
    queryset = Node.objects.select_related('tag', 'parent').all().order_by('id')
    serializer_class = NodeSerializer

class NodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.select_related('tag', 'parent').all().order_by('id')
    serializer_class = NodeSerializer

class TagTreeDetailView(views.APIView):
    Tree = TypedDict('Tree', {'name_ja': str, 'name_en': str, 'node_id': str, 'tag_id': str, 'tree_level': int, 'children': Optional[list['Tree']]})
    Node = TypedDict('Tree', {'name_ja': str, 'name_en': str, 'node_id': str, 'tag_id': str, 'parent_node_id': str})
    def get(self, request, pk):
        nodes = list(Node.objects.all().annotate(
            name_ja=F('tag__term_ja__name'),
            name_en=F('tag__term_en__name'),
            node_id=F('id'),
            parent_node_id=F('parent_id')
            ).values('node_id','parent_node_id', 'tag_id', 'name_ja', 'name_en'))
        try:
            root = Node.objects.annotate(
                name_ja=F('tag__term_ja__name'),
                name_en=F('tag__term_en__name'),
                node_id=F('id'),
                ).values('node_id', 'tag_id', 'name_ja', 'name_en').get(pk=pk)
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
