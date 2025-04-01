from django.shortcuts import render , get_object_or_404 , redirect
from django.views import View
from .models import Post , Like
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest


# Create your views here.

class BlogView(View):
    template_name ='blog/blog_page.html'

    def get(self,request):
        post = Post.objects.filter(status = 'p')
        return render(request , self.template_name , {'posts':post})

class PostDetailView(View):

    def get(self, request, slug, id):
        post = get_object_or_404(Post, id=id)
        user = request.user
        has_liked = False

        # بررسی وضعیت لایک
        if user.is_authenticated:
            has_liked = post.post_like.filter(user=user).exists()
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            has_liked = post.post_like.filter(session_key=session_key).exists()

        context = {
            'post': post,
            'has_liked': has_liked,
        }
        return render(request, 'blog/post_detail.html', context)


import uuid
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404

class LikePostView(View):

    def post(self, request, slug, id):
        post = get_object_or_404(Post, id=id)

        # ایجاد guest_id در کوکی در صورت نبود
        guest_id = request.COOKIES.get('guest_id')
        if not guest_id:
            guest_id = str(uuid.uuid4())  # شناسه یکتا برای مهمان
            request.session['guest_id'] = guest_id

        has_liked = False  # مقدار پیش‌فرض

        # بررسی درخواست AJAX
        if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
            return HttpResponseBadRequest("Invalid request")

        # مهمان
        if not request.user.is_authenticated:
            if Like.objects.filter(post=post, session_key=guest_id).exists():
                Like.objects.filter(post=post, session_key=guest_id).delete()
                has_liked = False
            else:
                Like.objects.create(post=post, session_key=guest_id)
                has_liked = True

        # کاربر لاگین کرده
        else:
            user = request.user
            if Like.objects.filter(post=post, user=user).exists():
                Like.objects.filter(post=post, user=user).delete()
                has_liked = False
            else:
                Like.objects.create(post=post, user=user)
                has_liked = True

        # محاسبه تعداد لایک
        like_count = Like.objects.filter(post=post).count()

        # تنظیم کوکی برای مهمان
        response = JsonResponse({'has_liked': has_liked, 'like_count': like_count})
        response.set_cookie('guest_id', guest_id)  # اعتبار یک ساله

        return response




            

    

        
            
        
        

        




        

        
    


