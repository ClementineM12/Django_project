"""AutoDash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http.response import HttpResponse
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls'), name='home'),
    path('upload/', include('upload.urls')),
    path('', RedirectView.as_view(url ='home/')),
    path("accounts/", include('django.contrib.auth.urls')),
    path('accounts/', include('login.urls')),
    path('visualization/', include('visualization.urls'), name='visualization'),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
    path('ml/', include('ml.urls'), name='ml'),
]
