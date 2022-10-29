from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_release, name = 'main' ),
    path('releases/', views.show_releases, name = 'releases' ),
    path('post/<int:post_id>/', views.show_post, name = 'post' ),
    path('release/<int:release_id>/', views.show_release, name = 'release' )
]
