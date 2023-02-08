from django.shortcuts import render
from .dash_apps import app1

# Create your views here.

def vizualization(request):
    return render(request, 'vizualization/vizualization.html')


