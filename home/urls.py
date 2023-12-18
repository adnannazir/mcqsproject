from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='dashboard'),
    path('partial_rendering', views.partial_rendering, name='partial_rendering'),
]
