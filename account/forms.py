from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegitrationForm(forms.Form):
    
    user_name = forms.CharField(label='نام کاربری',required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "نام کاربری "})) 
    email = forms.EmailField(label='ایمیل',required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "آدرس ایمیل"}))
    password = forms.CharField(label='رمز عبور' ,required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "رمز عبور"}))
    confirm_password = forms.CharField(label='تایید رمز عبور',required=False , widget=forms.TextInput(attrs={ "class": "single-field","placeholder": "تایید رمز عبور"}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if not email :
            raise ValidationError("لطفا فیلد را پر کنید")
        elif user :
            raise ValidationError('این ایمیل درحال حاضر وجود دارد')
        return email
    
    def clean_user_name(self):
        user_name = self.cleaned_data['user_name']
        user = User.objects.filter(username=user_name).exists()
        if not user_name :
             raise ValidationError("لطفا فیلد را پر کنید")
        elif user :
            raise ValidationError('نام کاربری تکراری است')
        
        return user_name
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('confirm_password')
        if not p1 or not p2:
            raise ValidationError("لطفا فیلد را پر کنید")
        elif p1 and p2 and p1 != p2 :
            raise ValidationError("رمزهای عبور باید مطابقت داشته باشند.")
        
        

        


        