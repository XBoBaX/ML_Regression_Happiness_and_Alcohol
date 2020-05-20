from django.shortcuts import render


def open_main(request):
    return render(request, 'linearReg/main.html', {"main": "dataset"})