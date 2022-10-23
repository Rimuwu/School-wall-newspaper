from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'main' ),
    path('post/<int:post_id>/', views.show_post, name = 'post' ),
    path('release/<int:release_id>/', views.show_release, name = 'release' )
]
