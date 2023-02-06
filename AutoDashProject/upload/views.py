from django.shortcuts import render, redirect
from .forms import DataForm
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile

# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save('documents/' + file.name, file)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload/upload.html')
    return render(request, 'upload/upload.html')