from django.shortcuts import render , redirect
from django.views import View
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth import authenticate 
from .forms import UserRegitrationForm

# Create your views here.

class RegisterView(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    template_name = 'account/user_register.html'
    form_class = UserRegitrationForm

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {'form':form})
        

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['user_name'], cd['email'], cd['password'])
            messages.success(request , "You registered successfully " , "success")
            return redirect('home:home')
        return render(request ,self.template_name , {"form" : form})
        