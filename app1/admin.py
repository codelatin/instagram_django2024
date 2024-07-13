from django.contrib import admin
from app1.models import Post, Stream,Tag


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display=("caption","posted","user")
    list_filter=["posted"]

class StreamAdmin(admin.ModelAdmin):
    list_display=("following","post","user","date")
    list_filter=["date"]

class TagAdmin(admin.ModelAdmin):
    list_display=("title","slug")


admin.site.register(Post, PostAdmin)
admin.site.register(Stream,StreamAdmin)
admin.site.register(Tag, TagAdmin)
