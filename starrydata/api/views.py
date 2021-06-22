from rest_framework import generics
from starrydata.models import FabricationProcess
from starrydata.api.serializers import FabricationProcessSerializer


class ListView(generics.ListCreateAPIView):
    queryset = FabricationProcess.objects.all().order_by('-id')
    serializer_class = FabricationProcessSerializer


class DetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FabricationProcess.objects.all()
    serializer_class = FabricationProcessSerializer
