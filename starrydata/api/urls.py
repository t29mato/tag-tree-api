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
]
