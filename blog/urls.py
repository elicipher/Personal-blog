from django.urls import path , re_path
from .views import BlogView, PostDetailView

app_name ='blog'
urlpatterns = [
    path('blog/',BlogView.as_view(), name='blog'),
    re_path(r'^post-detail/(?P<slug>[-\wآ-ی]+)/$',PostDetailView.as_view(), name='post_detail')
   
]
