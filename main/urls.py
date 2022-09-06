from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'home' ),
    path('post/<int:post_id>/', views.show_post, name = 'post' )
]
