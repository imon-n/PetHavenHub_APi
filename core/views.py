from django.shortcuts import render
from django.views.generic import TemplateView
from pets.models import CategoryModel,Pet_Model

def home(request, category_slug = None):
    data = Pet_Model.objects.all()
    categorys = CategoryModel.objects.all()
    if category_slug is not None:
        category_name = CategoryModel.objects.get(slug = category_slug)
        data = Pet_Model.objects.filter(category_name  = category_name)
    return render(request, 'home.html', {'data' : data, 'categorys':categorys})

def front(request):
    return render(request, 'front.html')

class HomeView(TemplateView):
    template_name = 'index.html'