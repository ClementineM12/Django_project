
"""AutoDashProject URL Configuration
"""
from django.http.response import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls'), name='home'),
    path('upload/', include('upload.urls')),
    path('', RedirectView.as_view(url ='home/')),
    path("accounts/", include('django.contrib.auth.urls')),
    path('accounts/', include('login.urls')),
    path('vizualization/', include('vizualization.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),
]

