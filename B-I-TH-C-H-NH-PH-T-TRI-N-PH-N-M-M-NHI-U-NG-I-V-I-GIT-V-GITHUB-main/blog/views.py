from django.shortcuts import render, get_object_or_404  
from .models import Post

def list(request):
    Data = {'Posts': Post.objects.all().order_by('-date')}
    return render(request, 'blog/blog.html', Data)

def post(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post.html', {'post': post})