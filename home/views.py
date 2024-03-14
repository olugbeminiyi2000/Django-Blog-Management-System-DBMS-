from django.shortcuts import render
from django.views import View


# Create your views here.
class HomeView(View):
    template = "home/main.html"
    def get(self, request):
        return render(request, self.template)
