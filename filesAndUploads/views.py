from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def upload_file(request):
    myfile = request.FILES['myfile']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    uploaded_file_url = fs.url(filename)
    print(uploaded_file_url)
    return render(request, 'linearReg/main.html', {"page": "dataset1", 'uploaded_file_url': uploaded_file_url})