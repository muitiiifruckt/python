from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('',views.index,name = "home"),
    path('game', views.game),
    path('about', views.about),
    path('contact', views.contact),
    path('news', views.news),
]
