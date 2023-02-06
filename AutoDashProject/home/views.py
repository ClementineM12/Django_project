from django.shortcuts import render


# Control the URLs that are associated with views inside the first_app

def home(request):
    return render(request, 'home/home.html')
