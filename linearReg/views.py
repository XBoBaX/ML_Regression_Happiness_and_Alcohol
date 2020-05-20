from django.shortcuts import render
from filesAndUploads.views import upload_file


def open_main(request):
    if request.method == 'POST' and request.FILES['myfile']:
        json = upload_file(request)
        json["page"] = "dataset"
        return render(request, 'linearReg/main.html', json)
    return render(request, 'linearReg/main.html', {"page": "dataset"})
