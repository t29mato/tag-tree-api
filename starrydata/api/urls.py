from django.urls import path
from starrydata.api import views

urlpatterns = [
    path('tags', views.TagListView.as_view(), name='TagListView'),
    path('tags/<int:pk>', views.TagDetailView.as_view(), name='TagDetailView'),
    path('nodes', views.NodeListView.as_view(), name='polyerNodeList'),
    path('nodes/<int:pk>', views.NodeDetailView.as_view(), name='NodeDetailView'),
    # TODO: tag_tree should be tag_trees
    path('tag_tree', views.TagTreeListView.as_view(), name='TagTreeListView'),
    path('tag_tree/<int:pk>', views.TagTreeDetailView.as_view(), name='TagTreeDetailView'),
]
