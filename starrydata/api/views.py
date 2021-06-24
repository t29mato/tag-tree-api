from rest_framework import generics
from starrydata.models import FabricationProcess, SynthesisMethodTag, SynthesisMethodTagTreeNode
from starrydata.api.serializers import FabricationProcessSerializer, SynthesisMethodTagSerializer, SynthesisMethodTagTreeNodeSerializer


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
