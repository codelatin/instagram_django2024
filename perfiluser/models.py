from django.db import models
from django.contrib.auth.models import User 
from app1.models import Post

# Create your models here.
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True, blank=True) 
    last_name = models.CharField(max_length=50, null=True, blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    url = models.URLField(max_length=1000, null=True, blank=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    imagen = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name="Picture")
    favorite = models.ManyToManyField(Post)
    
    