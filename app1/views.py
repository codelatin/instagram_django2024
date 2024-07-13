
from django.shortcuts import render, redirect, get_object_or_404
from app1.models import Post, Stream, Tag, Likes
from django.contrib.auth.decorators import login_required
from app1.forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from perfiluser.models import Profile



# Create your views here.

def index(request):
    user = request.user
    posts= Stream.objects.filter(user=user)
    group_ids= []
    for post in posts:
        group_ids.append(post.post_id)
    post_items= Post.objects.filter(id__in=group_ids).all().order_by('-posted')
    context ={
        'post_items': post_items
    }
    return render(request, 'index.html', context)


def newPost(request):
    user = request.user.id
    tags_obj = [] #Se inicializa una lista vacía para almacenar los objetos de etiqueta
    if request.method == 'POST':  #Se verifica si la solicitud es de tipo POST
        form = PostForm(request.POST, request.FILES) #Se crea una instancia de PostForm con los datos de la solicitud POST y los archivos adjuntos
        #Verificamos si el formulario es válido
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')
            
            tags_list = list(tags_form.split(','))
            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title = tag)
                tags_obj.append(t)
            p, created = Post.objects.get_or_create(picture = picture, caption = caption, user_id = user)
            p.tags.set(tags_obj)      
            p.save()      
            return redirect('index')
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, "newPost.html", context) 

def details_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    context = {
        "post": post
    }
    return render(request, "details_post.html", context)

def tags(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tag=tag).order_by('-posted')
    context = {
        "tag": tag,
        "posts": posts
    }
    return render(request, "tags.html", context)

def like(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    liked = Likes.objects.filter(user=user, post=post).count()
    if not liked:
        Likes.objects.create(user=user, post=post)
        current_likes = current_likes + 1
    else:
        Likes.objects.filter(user=user, post=post).delete()
        current_likes = current_likes - 1
    post.likes = current_likes
    post.save()
        
    return HttpResponseRedirect(reverse('details_post', args=[post_id]))

def favorite(request, post_id):
    user = request.user
    post = Post.objects.get(id=post_id) 
    profile = Profile.objects.get(user=user)
    if profile.favorite.filter(id=post_id).exists():
        profile.favorite.remove(post)
    else:
        profile.favorite.add(post)
        
    return HttpResponseRedirect(reverse('details_post', args=[post_id]))

