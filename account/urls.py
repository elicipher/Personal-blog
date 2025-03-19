from django.urls import  path
from .views import RegisterView , LoginView , LogoutView , EditProfileView

app_name = 'account'
urlpatterns = [
    path('register/', RegisterView.as_view() , name='user_register'),
    path('login/', LoginView.as_view() , name='user_login'),
    path('logout/', LogoutView.as_view() , name='user_logout'),
    path('profile/', EditProfileView.as_view() , name='user_profile'),
]