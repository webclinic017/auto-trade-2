from django.urls import path

from . import views

app_name = 'trade'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.query, name='query'),
    path('query/', views.query, name='query'),
]