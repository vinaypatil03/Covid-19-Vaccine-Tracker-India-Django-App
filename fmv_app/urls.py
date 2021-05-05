from django.urls import path
from . import views
# from django.conf import settings
# from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name="home"),
    path('getdistrict/', views.getDistrict, name="getdistrict"),
    path('findbypin/', views.findByPin, name="findbypin"),
    path('findbydistrict/', views.findByDistrict, name="findbydistrict")
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
