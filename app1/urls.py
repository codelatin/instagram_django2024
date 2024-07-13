from django.urls import path

from app1.views import * #se importan todas las vistas

urlpatterns = [
    path('', index, name='index'),
    path('newPost/', newPost, name='newPost'),
    path('<uuid:post_id>/', details_post, name='details_post'),
    path('tag/<slug:tag_slug>', tags, name='tags'),
    path('<uuid:post_id>/like', like, name='like'),
    path('<uuid:post_id>/favorite', favorite, name='post-favorite'),
]

