from django.shortcuts import render
from filesAndUploads.views import upload_file


def open_main(request):
    if request.method == 'POST' and request.FILES['myfile']:
        upload_file(request)
    return render(request, 'linearReg/main.html', {"main": "dataset"})