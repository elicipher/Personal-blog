from django.urls import path
from .views import BlogView, PostDetailView

app_name ='blog'
urlpatterns = [
    path('blog/',BlogView.as_view(), name='blog'),
    path('post-detail/',PostDetailView.as_view(), name='post_detail')
]