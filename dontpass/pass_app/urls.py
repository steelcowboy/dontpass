from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:cls>', views.class_lookup, name='class_lookup'),
    path('api/class_list', views.list_classes, name='list_classes'),
]
