from django.urls import path
from starrydata.api import views

urlpatterns = [
    path('databases', views.DatabaseListView.as_view(), name='databaseList'),
    path('papers', views.PaperListView.as_view(), name='paperList'),
    path('figures', views.FigureListView.as_view(), name='figureList'),
    path('samples', views.SampleListView.as_view(), name='sampleList'),
    path('tags', views.TagListView.as_view(), name='TagListView'),
    path('tags/<int:pk>', views.TagDetailView.as_view(), name='TagDetailView'),
    path('nodes', views.NodeListView.as_view(), name='polyerNodeList'),
    path('nodes/<int:pk>', views.NodeDetailView.as_view(), name='NodeDetailView'),
    path('tag_tree/<int:pk>', views.TagTreeDetailView.as_view(), name='TagTreeDetailView'),
    path('fabrication_processes', views.ListView.as_view(), name='processList'),
    path('fabrication_processes/<int:pk>', views.DetailView.as_view(), name='processDetail'),
    path('synthesis_method_tags', views.SynthesisMethodTagListView.as_view() , name='SynthesisMethodTagList'),
    path('synthesis_method_tags/<int:pk>', views.SynthesisMethodTagDetailView.as_view(), name='SynthesisMethodTagDetail'),
    path('synthesis_method_tag_tree_nodes', views.SynthesisMethodTagTreeNodeListView .as_view() , name='SynthesisMethodTagTreeNodeList'),
    path('synthesis_method_tag_tree_nodes/<int:pk>', views.SynthesisMethodTagTreeNodeDetailView.as_view(), name='SynthesisMethodTagTreeNodeDetail'),
]
