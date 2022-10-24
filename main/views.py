from django.shortcuts import redirect, render

from .models import Post, Release


def index(request):

    releases = Release.objects.filter(visibility = 1).order_by('position')
    first_post = None
    one_colum_posts, two_colum_posts = [], []
    big_one_post, big_two_post = None, None

    if len(releases) != 0:
        fisrt_release = releases[0]
        posts = fisrt_release.posts.all()

        for n in range(0, 7):

            try:
                if n == 0:
                    first_post = posts[n]
                
                elif n < 3:
                    one_colum_posts.append( posts[n] )
                
                elif n == 3:
                    big_one_post = posts[n]
                
                elif n < 6:
                    two_colum_posts.append( posts[n] )
                
                else:
                    big_two_post  = posts[n]
            except: pass

    else:
        fisrt_release = None

    return render( request, 'main/index.html',
            { "release": fisrt_release,
              "first_post": first_post,
              'one_colum_posts': one_colum_posts,
              'two_colum_posts': two_colum_posts,
              'big_one_post': big_one_post,
              'big_two_post': big_two_post,
              'members': fisrt_release.members.all()
            }
    )


def show_release(request, release_id):

    releases = Release.objects.filter(id = release_id)
    first_post = None
    one_colum_posts, two_colum_posts = [], []
    big_one_post, big_two_post = None, None

    if len(releases) != 0:
        fisrt_release = releases[0]
        posts = fisrt_release.posts.all()

        for n in range(0, 7):

            try:
                if n == 0:
                    first_post = posts[n]
                
                elif n < 3:
                    one_colum_posts.append( posts[n] )
                
                elif n == 3:
                    big_one_post = posts[n]
                
                elif n < 6:
                    two_colum_posts.append( posts[n] )
                
                else:
                    big_two_post  = posts[n]
            except: pass

    else:
        fisrt_release = None

    return render( request, 'main/index.html',
            { "release": fisrt_release,
              "first_post": first_post,
              'one_colum_posts': one_colum_posts,
              'two_colum_posts': two_colum_posts,
              'big_one_post': big_one_post,
              'big_two_post': big_two_post,
              'members': fisrt_release.members.all()
            }
    )


def show_post(request, post_id):
    post = Post.objects.filter(id = post_id)[0]
    release = Release.objects.filter(posts = post)[0]

    return render( request, 'main/post.html',
            { 'release': release,
              'post': post,
            }
    )

def releases(request):
    releases = Release.objects.filter(visibility = 1).order_by('position')

    return render( request, 'main/releases.html',
            { "releases": releases,
            }
    )

