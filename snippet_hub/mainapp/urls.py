from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('snippet/create/', views.create_snippet, name='create_snippet')
]
