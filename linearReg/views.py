from django.shortcuts import render
from filesAndUploads.views import upload_file


def open_main(request):
    json = {}
    if request.method == 'POST' and request.POST.get('id_edit') != None:
        print(request.POST.get('filename'))
        json = upload_file(request, request.POST.get('filename'))
        mylist = list(json["mylist"])
        print(mylist[int(request.POST.get('id_edit'))][0])
        if request.POST.get('country_edit') != "":
            country = request.POST.get('country_edit')
        else:
            country = mylist[int(request.POST.get('id_edit'))][0]
        if request.POST.get('Happy_edit') != "":
            hap = request.POST.get('Happy_edit')
        else:
            hap = mylist[int(request.POST.get('id_edit'))][1]
        if request.POST.get('Beer_edit') != "":
            beer = request.POST.get('Beer_edit')
        else:
            beer = mylist[int(request.POST.get('id_edit'))][2]
        tulpe = (country, hap, beer)
        mylist[int(request.POST.get('id_edit'))] = tulpe
        json["mylist"] = mylist
    elif request.method == 'POST' and request.FILES['myfile']:
        json = upload_file(request, "")

    json["page"] = "dataset"
    return render(request, 'linearReg/main.html', json)