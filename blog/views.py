from django.shortcuts import render , get_object_or_404 , redirect , HttpResponseRedirect
from django.views import View
from .models import Post , Like , PostVisit
from django.urls import reverse
from django.http import JsonResponse
from .forms import CommentForm
from django.contrib import messages





# Create your views here.

class BlogView(View):
    template_name ='blog/blog_page.html'

    def get(self,request):
        post = Post.objects.filter(status = 'p')
        return render(request , self.template_name , {'posts':post})

class PostDetailView(View):

    class_form = CommentForm
    def get(self, request, slug, id):
        
        form =self.class_form()
        post = get_object_or_404(Post, id=id , slug = slug)
        user = request.user
        comment = post.postcomment.filter(confirme = True)
        has_liked = False #مقدار پیش فرض 
        x_forwarded_for  = request.META.get('X-Forwarded-For')
        if x_forwarded_for :
            ip = x_forwarded_for.split(',')[0] #گرفتن اولین آی پی که آی پی اصلی کاربره
        else :
            ip = request.META.get('REMOTE_ADDER')

        if not PostVisit.objects.filter(post=post ,ip_address =ip).exists():
            PostVisit.objects.create(post=post, ip_address=ip)
        if user.is_authenticated :
            if Like.objects.filter(user = user , post = post).exists():
                has_liked = True
        return render(request, 'blog/post_detail.html',{'comment':comment,'post': post , 'has_liked':has_liked , 'like_count':post.like_count() , 'form':form})
    
    def post(self , request ,slug, id ):
        post = get_object_or_404(Post, id=id , slug = slug)
        form =self.class_form(request.POST)
        
        
           
        if form.is_valid:
            if not request.user.is_authenticated:
                next_url = reverse('blog:post_detail', kwargs={'slug': slug, 'id': id})
                login_url = reverse("account:user_login")  # مسیر لاگین
                return HttpResponseRedirect(f"{login_url}?next={next_url}")
            else :
                new_comment = form.save(commit= False)
                new_comment.user = request.user
                new_comment.post = post
                new_comment.confirme = False
                new_comment.save()

        messages.success(request , "کامنت شما ثبت شد و پس از تأیید نمایش داده می‌شود.")
        return redirect('blog:post_detail' , post.slug , post.id)
        

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

