import json
from json.decoder import JSONDecodeError
from typing import Optional, TypedDict
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from django.db.models import F
from starrydata.models import Database, FabricationProcess, Figure, Paper, PolymerTag, PolymerNode, Sample, SynthesisMethodTag, SynthesisMethodTagTreeNode
from starrydata.api.serializers import DatabaseSerializer, FigureSerializer, PaperSerializer, FabricationProcessSerializer, PolymerTagSerializer, PolymerNodeSerializer, SampleSerializer, SynthesisMethodTagSerializer, SynthesisMethodTagTreeNodeSerializer, PolymerTagTreeSerializer

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


class PolymerTagListView(generics.ListCreateAPIView):
    queryset = PolymerTag.objects.all()
    serializer_class = PolymerTagSerializer
    search_fields = ['name']

class PolymerTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PolymerTag.objects.all()
    serializer_class = PolymerTagSerializer

class PolymerNodeListView(generics.ListCreateAPIView):
    queryset = PolymerNode.objects.all()
    serializer_class = PolymerNodeSerializer

class PolymerNodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PolymerNode.objects.all()
    serializer_class = PolymerNodeSerializer

class PolymerTagTreeView(views.APIView):
    get_serializer = PolymerTagTreeSerializer
    Tree = TypedDict('Tree', {'name': str, 'node_id': str, 'polymer_tag_id': str, 'children': Optional[list['Tree']]})
    Node = TypedDict('Tree', {'name': str, 'node_id': str, 'polymer_tag_id': str, 'parent_node_id': str})
    def get(self, request, *args, **kwargs):
        nodes = list(PolymerNode.objects.all().annotate(name=F('polymer_tag__name'), node_id=F('id'), tag_id=F('polymer_tag_id'), parent_node_id=F('parent_id')).values('node_id', 'parent_node_id', 'polymer_tag_id', 'name'))
        root = PolymerNode.objects.filter(id=kwargs['pk']).annotate(name=F('polymer_tag__name'), node_id=F('id'), tag_id=F('polymer_tag_id')).values('node_id', 'polymer_tag_id', 'name')[0]
        tree = self.__generateTree(root, nodes)
        serializer = PolymerTagTreeSerializer(data=tree)
        # テストの実装
        try:
            if not serializer.is_valid():
                raise ValueError("シリアライズのバリデーションに失敗", serializer.errors)
        except ValueError as e:
            print(e)
        return Response(serializer.data, status=200)

    # FIXME: type hint
    def __generateTree(self, parent: Tree, nodes: Node):
        children = list(filter(lambda node: node['parent_node_id'] == parent['node_id'], nodes))
        parent['children'] = list(map(lambda child: self.__generateTree(child, nodes), children))
        return parent

class ListView(generics.ListCreateAPIView):
    queryset = FabricationProcess.objects.all().order_by('-id')
    serializer_class = FabricationProcessSerializer


class DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FabricationProcess.objects.all()
    serializer_class = FabricationProcessSerializer

class SynthesisMethodTagListView(generics.ListCreateAPIView):
    queryset = SynthesisMethodTag.objects.all().order_by('-id')
    serializer_class = SynthesisMethodTagSerializer

class SynthesisMethodTagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SynthesisMethodTag.objects.all()
    serializer_class = SynthesisMethodTagSerializer

class SynthesisMethodTagTreeNodeListView(generics.ListCreateAPIView):
    queryset = SynthesisMethodTagTreeNode.objects.all().order_by('-id')
    serializer_class = SynthesisMethodTagTreeNodeSerializer

class SynthesisMethodTagTreeNodeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SynthesisMethodTagTreeNode.objects.all()
    serializer_class = SynthesisMethodTagTreeNodeSerializer
