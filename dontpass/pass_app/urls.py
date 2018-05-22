from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:cls>', views.class_lookup, name='class_lookup'),
]
