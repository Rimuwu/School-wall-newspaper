from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import LinkPosts, Post, Release


def show_release(request, slug=None):

    if slug is not None:
        release = get_object_or_404(Release, slug=slug)
    else:
        releases = Release.objects.filter(visibility=1).order_by('position')
        release = releases[0]
    
    if not (release.visibility or request.user.is_authenticated):
        raise Http404()
    else:
        if slug != None and release.position == 1:
            return redirect('/')
        else:
            return render(request, 'main/release.html', {'release': release})


def show_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    link_set = LinkPosts.objects.filter(post_link=post)
    release, buttons = None, []

    if len(link_set) > 0:
        release = link_set[0].release_link
        buttons = release.get_pagination(slug)

    is_authenticated = request.user.is_authenticated
    exists_release = release != None

    if exists_release and not (release.visibility or is_authenticated):
        raise Http404()
    elif not (exists_release or is_authenticated):
        raise Http404()
    else:
        return render(request, 'main/post.html',
                     {'release': release,
                      'post': post,
                      'buttons': buttons
                     })


def show_releases(request):

    if request.user.is_authenticated:
        releases = Release.objects.order_by('position')
    else:
        releases = Release.objects.filter(visibility=1).order_by('position')
        
    return render(request, 'main/releases.html', {"releases": releases})

def error_403(request, exception):

    response = render(request, 'main/errors/403.html')
    response.status_code = 403
    return response

def error_404(request, exception):

    response = render(request, 'main/errors/404.html')
    response.status_code = 404
    return response

def error_500(request):

    response = render(request, 'main/errors/500.html')
    response.status_code = 500
    return response

