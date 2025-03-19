from django.shortcuts import render , redirect
from django.views import View
from .models import Member
from django.contrib import messages
from django.contrib.auth import login , logout
from .forms import UserRegitrationForm , UserLoginForm ,EditProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin

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
            full_name = cd.get('full_name')
            user_name = cd.get("user_name")
            email = cd.get('email')
            password = cd.get('password')
            new_member = Member(full_name=full_name , username = user_name , email = email )
            new_member.set_password(password)
            new_member.save()
            login(self.request,new_member)
            messages.success(request , "ثبت نام با موفقیت انجام شد" , "success")
            return redirect('home:home')
        return render(request ,self.template_name , {"form" : form})

class LoginView(View):
    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated :
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    template_name = 'account/user_login.html'
    form_class = UserLoginForm

    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name , {"form": form})

    def post(self , request):
        form = self.form_class(request.POST)
        if form.is_valid():
    
            login(request , form.user)
            messages.success(request ,"شما با موفقیت وارد حساب کاربریتان شدید  " , "success")
            if self.next:
                return redirect(self.next)
            return redirect('home:home')
        
        return render(request , self.template_name , {"form": form})


class LogoutView(LoginRequiredMixin , View):
        def get(self,request):
            logout(self.request)
            messages.success(request , "شما با موفقیت از حساب کاربریتان خارج شدید" , "success")
            return redirect('home:home')


class EditProfileView(LoginRequiredMixin,View):
    form_class = EditProfileForm
    template_name = 'account/user_profile.html'
    
    def get(self , request):
        form = self.form_class(instance=request.user , initial={"full_name":request.user.full_name ,'email':request.user.email , "avatar":request.user.avatar})
        return render(request , self.template_name , {'form': form})

    def post(self, request):
        form = self.form_class(request.POST , request.FILES , instance = request.user)
        if form.is_valid():
            form.save()
            request.user.full_name = form.cleaned_data['full_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request , "پروفایل شما با موفقیت عوض شد" , 'success')
        return redirect("account:user_profile")
