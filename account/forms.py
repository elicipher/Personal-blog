from django import forms
from .models import Member
from django.core.exceptions import ValidationError 
from django.contrib.auth import authenticate


class UserRegitrationForm(forms.Form):
    full_name = forms.CharField(label='نام و نام خانوادگی',required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "نام و نام خانوادگی"}))
    user_name = forms.CharField(label='نام کاربری',required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "نام کاربری "})) 
    email = forms.EmailField(label='ایمیل',required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "آدرس ایمیل"}))
    password = forms.CharField(label='رمز عبور' ,required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "رمز عبور"}))
    confirm_password = forms.CharField(label='تایید رمز عبور',required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "تایید رمز عبور"}))
    
    def clean(self):
        cd = super().clean()
        full_name = cd.get("full_name")
        if not full_name :
            self.add_error("full_name", "لطفا فرم را پر کنید")

        user_name = cd.get("user_name")
        user = Member.objects.filter(username = user_name).exists()
        if not user_name:
            self.add_error("user_name","لطفا فرم را پر کنید")
        elif user :
            self.add_error("user_name","نام کاربری تکراری است")
        
        
        email = cd.get("email")
        email_exists = Member.objects.filter(email = email).exists()
        if not email :
            self.add_error("email","لطفا فرم را پر کنید")
        elif email_exists :
            self.add_error("email","ایمیل درحال حاضر وجود دارد")

        password = cd.get("password")
        confirm_password = cd.get("confirm_password")

        if not password:
            self.add_error("password","لطفا رمز عبور را وارد کنید")
        elif not confirm_password :
            self.add_error("confirm_password","لطفا فرم را پرکنید ")
        elif confirm_password != password:
            self.add_error("confirm_password","رمزهای عبور باید مطابقت داشته باشند ")
        elif len(password) <= 8 :
            self.add_error("password","رمز عبور باید بیشتر از ۸ تا کارکتر باشد")
        
        cd.pop("confirm_password", None)
        return cd

        
class UserLoginForm(forms.Form):
    user_name = forms.CharField(label='نام کاربری',required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "ایمیل یا نام کاربری"})) 
    password = forms.CharField(label='رمز عبور' ,required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "رمز عبور"}))

    def clean(self):
        cd = super().clean()
        user_name= cd.get("user_name")
        password= cd.get("password")
        user = authenticate(username = user_name , password =password )
       
        if not password or not user_name  :
            raise ValidationError("لطفا فرم را پر کنید")
        if user is None :
            raise ValidationError("نام کاربری یا رمز عبور اشتباه است")

        self.user = user  # کاربر معتبر را ذخیره می‌کنیم تا در ویو استفاده شود
        
        return cd
    
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ('avatar','full_name','username','email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام کاربری'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ایمیل'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام و نام خانوادگی'}),
            
        }
        labels = {
            'username': ':نام کاربری ',
            'email': ':ایمیل',
            'full_name':  ':نام',
            'avatar': ' :تصویر پروفایل',
        }

    


        






        