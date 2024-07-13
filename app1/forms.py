from django import forms
from app1.models import Post

class PostForm(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TimeInput(
        attrs= {'class': 'input','placeholder': 'Write a Caption'}), required=True)
    tags = forms.CharField(widget=forms.TimeInput(
        attrs= {'class': 'input','placeholder': 'Etiquetas | separadas por coma'}), required=True)
    
    class Meta:
        model = Post
        fields = ['picture', 'caption', 'tags']
        
    