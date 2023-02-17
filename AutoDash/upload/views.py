from django.shortcuts import render, redirect
from .forms import DataForm
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from .forms import DataForm
from .models import Data

# Create your views here.


def upload_file(request):
    if request.method == 'POST':
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save('documents/' + file.name, file)
        uploaded_file_url = fs.url(filename)
        fileObj = Data(document=file.name)
        fileObj.save()
        lastObj = Data.objects.all().last()
        return render(request, 'upload/upload.html')
    return render(request, 'upload/upload.html')

# def upload_file(request):
#     if request.method == 'POST':
#         form = DataForm(request.POST,request.FILES)
#         print(form)
#         if form.is_valid():
#             form.save()
#             print('is valid and saved')
#             return redirect('visualization')
#     else:
#         form = DataForm()        
#     return render(request, 'upload/upload.html', {'form':form})