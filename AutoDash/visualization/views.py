from django.shortcuts import render, redirect
from .dash_apps import app1

# Create your views here.

def visualization(request):
    return render(request, 'visualization/visualization.html')

