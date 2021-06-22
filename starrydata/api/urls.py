from django.urls import path
from starrydata.api import views

urlpatterns = [
    path('processes/', views.ListView.as_view(), name='processList'),
    path('processes/<int:pk>', views.DetailView.as_view(), name='processDetail')
]
