from django.urls import path
from starrydata.api import views

urlpatterns = [
    path('tags', views.TagListView.as_view(), name='TagListView'),
    path('tags/<int:pk>', views.TagDetailView.as_view(), name='TagDetailView'),
    path('nodes', views.NodeListView.as_view(), name='polyerNodeList'),
    path('terms', views.TermListView.as_view(), name='TermListView'),
    path('nodes/<int:pk>', views.NodeDetailView.as_view(), name='NodeDetailView'),
    path('tag_tree/<int:pk>', views.TagTreeDetailView.as_view(), name='TagTreeDetailView'),
    path('tag_ancestors/<int:pk>', views.TagAncestorsView.as_view(), name='TagAncestorsView'),
]
