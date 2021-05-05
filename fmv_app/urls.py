from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('getdistrict/', views.getDistrict, name="getdistrict"),
    path('findbypin/', views.findByPin, name="findbypin"),
    path('findbydistrict/', views.findByDistrict, name="findbydistrict")
]
