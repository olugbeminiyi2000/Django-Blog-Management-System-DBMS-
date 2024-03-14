from django.forms import ModelForm
from .models import BlogCategory, BlogPost

class BlogForm(ModelForm):
    class Meta:
        model = BlogPost
        fields = "__all__"

class CategoryForm(ModelForm):
    class Meta:
        model = BlogCategory
        fields = "__all__"

