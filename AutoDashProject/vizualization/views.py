from django.shortcuts import render

# Create your views here.

def vizualization(request):
    return render(request, 'vizualization/vizualization.html')