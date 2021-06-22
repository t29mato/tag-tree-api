from django.urls import path
from starrydata.api import views

urlpatterns = [
    path('fabrication_processes/', views.ListView.as_view(), name='processList'),
    path('fabrication_processes/<int:pk>', views.DetailView.as_view(), name='processDetail')
]
