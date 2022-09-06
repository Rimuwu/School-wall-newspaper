from django.shortcuts import render, redirect
from .models import Note

def index(request):
    notes = Note.objects.order_by('id')

    return render( request, 'main/index.html',
            { 'title': 'Главная страница сайта',
              'notes': notes,
            }
                 )

def show_post(request, post_id):
    return render( request, 'main/post.html',
                    { 'title': f'Отображение статьи с id {post_id}'}
           )
