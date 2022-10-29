from turtle import pos
from django.shortcuts import render

from .models import Post, Release, LinkPosts, LinkUsers


def show_release(request, release_id = None):
    release = None
    posts = []
    users = []

    if release_id != None:
        releases = Release.objects.filter(id = release_id)

    else:
        releases = Release.objects.filter(visibility = 1).order_by('position')

    if len(releases) != 0:
        release = releases[0]
        posts_links = LinkPosts.objects.filter(release_link = release).order_by('position')
        users = LinkUsers.objects.filter(release_link = release).order_by('position')

        for post in posts_links:
            posts.append(post.post_link)

    return render( request, 'main/release.html',
            { 'release': release,
              'posts': posts,
              'members': users
            }
    )


def show_post(request, post_id):
    post = Post.objects.filter(id = post_id)[0]
    link_set = LinkPosts.objects.filter(post_link = post)
    
    if len(link_set) > 0:
        release = link_set[0].release_link
    else:
        release = None

    return render( request, 'main/post.html',
            { 'release': release,
              'post': post,
            }
    )

def show_releases(request):
    releases = Release.objects.filter(visibility = 1).order_by('position')

    return render( request, 'main/releases.html',
            { "releases": releases,
            }
    )

