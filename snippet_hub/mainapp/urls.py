from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('snippet/create/', views.create_snippet, name='create_snippet'),
    path('snippets/my/', views.main_snippets, name='main_snippets'),
    path('snippets/<int:id>/', views.snippet_detail, name='snippet_detail'),
    path('signup/', views.sign_up, name ='signup'),
    path('profile/', views.profile, name='profile'),
]
