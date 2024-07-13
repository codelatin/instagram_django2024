from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.urls import resolve,reverse
from app1.models import Post,Follow,Stream
from perfiluser.models import Profile
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponseRedirect



# Create your views here.
#Esta vista es para perfil de cada USUARIO
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    url_name = resolve(request.path).url_name
    if url_name == "profile":
        posts = Post.objects.filter(user=user).order_by('-posted')
    else:
        posts = profile.favorite.all()

    #variables seguidores y posts
    count_post= Post.objects.filter(user=user).count()
    count_following=Follow.objects.filter(follower=user).count()
    count_followers= Follow.objects.filter(following=user).count()

    #status seguidores:
    follow_status= Follow.objects.filter(following=user, follower=request.user).exists()

        
    paginator = Paginator(posts, 3)
    
    page_number = request.GET.get("page")
    posts_paginator = paginator.get_page(page_number)
    context ={
        "posts_paginator": posts_paginator,
        "profile": profile,
        "posts": posts,
        "url_name": url_name,
        "count_post":count_post,
        "count_following":count_following,
        "count_followers":count_followers,
        "follow_status":follow_status
    }
    
    return render(request, 'profile.html', context)


def follow(request, username, option):
    user = request.user
    following = get_object_or_404(User, username=username)
    try:
        fo, created = Follow.objects.get_or_create(follower=user, following=following)
        if int(option) == 0:
            fo.delete()
            Stream.objects.filter(following=following, user=user).all().delete()
        else:
            posts = Post.objects.filter(user=following)[:10]

            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.posted, following=following)
                    stream.save()
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))


