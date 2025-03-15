from django.shortcuts import render
from django.views import View
# Create your views here.

class HomeView(View):
    template_name = 'home/index.html'

    def get(self,requset):
        return render(requset , self.template_name)
    

