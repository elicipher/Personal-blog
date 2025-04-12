from django.shortcuts import render
from django.views import View 
from django.views.generic.edit import CreateView 
from .forms import ContactForm
from django.contrib import messages
from .models import Contact

# Create your views here.

class HomeView(View):
    template_name = 'home/index.html'
    form_class = ContactForm  

    def get(self,requset):
        form = self.form_class()
        return render(requset , self.template_name , {'form':form})
    
class ContactView(CreateView):
    model = Contact
    form_class = ContactForm   
    template_name = 'home/index.html'
    success_url = '/'

    def form_valid(self, form):
        messages.success(self.request, "پیام شما با موفقیت ارسال شد 😊")
        return super().form_valid(form)
    



