from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from app import views




urlpatterns = [

    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('',views.index,name = "home"),
    path('game', views.game),
    path('about', views.about),
    path('contact', views.contact),
    path('news', views.news),
    path('make_move', views.make_move, name='make_move'),
    path('signup/', views.registration, name='registration'),
]
