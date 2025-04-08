from django.shortcuts import render , get_object_or_404 , redirect
from django.views import View
from .models import Post , Like , PostVisit
from django.urls import reverse
from django.http import JsonResponse




# Create your views here.

class BlogView(View):
    template_name ='blog/blog_page.html'

    def get(self,request):
        post = Post.objects.filter(status = 'p')
        return render(request , self.template_name , {'posts':post})

class PostDetailView(View):


    def get(self, request, slug, id):
        post = get_object_or_404(Post, id=id , slug = slug)
        user = request.user
        has_liked = False #مقدار پیش فرض 
        ip_address = request.META.get('X-Forwarded-For')
        if not PostVisit.objects.filter(post=post ,ip_address = ip_address).exists():
            PostVisit.objects.create(post=post, ip_address=ip_address)
        if user.is_authenticated :
            if Like.objects.filter(user = user , post = post).exists():
                has_liked = True
            
            

        return render(request, 'blog/post_detail.html',{'post': post , 'has_liked':has_liked , 'like_count':post.like_count()})




class LikePostView(View):

    def post(self, request, slug, id):
        post = get_object_or_404(Post, id=id, slug=slug)
        user = request.user
        
        if not user.is_authenticated:
           
            next_url = reverse('blog:post_detail', kwargs={'slug': slug, 'id': id})
            login_url = reverse("account:user_login")  # مسیر لاگین
            return JsonResponse({'status': 'unauthenticated', 'login_url': login_url, 'next_url': next_url})
            
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()
            return JsonResponse({'status': 'unliked', 'like_count':post.like_count()})
        
        return JsonResponse({'status': 'liked', 'like_count':post.like_count() })

     








            

    

        
            
        
        

        




        

        
    


