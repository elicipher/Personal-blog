from django.shortcuts import render
from django.views import View
# Create your views here.

class BlogView(View):
    template_name ='blog_page.html'

    def get(self,request):
        return render(request , self.template_name)

class PostDetailView(View):
    template_name = 'post_detail.html'

    def get(self , request):
        return render(request , self.template_name)


