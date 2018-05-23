from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tanner', views.tanner, name='tanner'),
    path('eric', views.eric, name='eric'),
    path('amanda', views.amanda, name='amanda'),
    path('<slug:cls>', views.class_lookup, name='class_lookup'),
    path('api/class_list', views.list_classes, name='list_classes'),
]
