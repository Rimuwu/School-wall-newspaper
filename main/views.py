from django.http import Http404
from django.shortcuts import get_object_or_404, render

from .models import LinkPosts, Post, Release


def show_release(request, slug=None):

    if slug is not None:
        release = get_object_or_404(Release, slug=slug)
    else:
        releases = Release.objects.filter(visibility=1).order_by('position')
        release = releases[0]
    
    if release.visibility == False and request.user.is_authenticated == False:
        raise Http404()
    else:
        return render(request, 'main/release.html', {'release': release})


def show_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    link_set = LinkPosts.objects.filter(post_link=post)
    release = None

    if len(link_set) > 0:
        release = link_set[0].release_link
        buttons = release.get_pagination(slug)
    
    if post.visibility == False and request.user.is_authenticated == False:
        raise Http404()
    else:
        return render(request, 'main/post.html',
                    {'release': release,
                     'post': post,
                     'buttons': buttons
                    })


def show_releases(request):
    releases = Release.objects.filter(visibility=1).order_by('position')
    return render(request, 'main/releases.html', {"releases": releases})
