from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def upload_file(request):
    myfile = request.FILES['myfile']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    return render(request, 'linearReg/main.html', {"main": "dataset", 'uploaded_file_url': uploaded_file_url})