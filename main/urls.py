from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_release, name = 'main' ),
    path('releases/', views.show_releases, name = 'releases' ),
    path('post/<str:slug>/', views.show_post, name = 'post' ),
    path('release/<str:slug>/', views.show_release, name = 'release' )
]
