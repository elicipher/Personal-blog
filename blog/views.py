from django.shortcuts import render , get_object_or_404
from django.views import View
from .models import Post

# Create your views here.

class BlogView(View):
    template_name ='blog/blog_page.html'

    def get(self,request):
        post = Post.objects.filter(status = 'p')
        return render(request , self.template_name , {'posts':post})

class PostDetailView(View):
    template_name = 'blog/post_detail.html'
    
    def get(self , request , slug):
        post = get_object_or_404(Post ,slug = slug )
        return render(request , self.template_name , {'post':post})


