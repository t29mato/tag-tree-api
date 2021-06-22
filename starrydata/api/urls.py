from django.urls import path
from starrydata.api import views

urlpatterns = [
    path('processes/', views.ListView.as_view(), name='processes')
]
