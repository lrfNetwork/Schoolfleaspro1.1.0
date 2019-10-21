from django.urls import path
from apps.collect import views

urlpatterns = [
    path('index/', views.index, name="index"),
    path('search/', views.search, name="search")
]