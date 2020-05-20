from django.shortcuts import render
from filesAndUploads.views import upload_file


def open_main(request):
    json = {}
    if request.method == 'POST' and request.POST.get('id_edit') is not None:
        json = edit_table(request)
    elif request.method == 'POST' and request.FILES['my_file']:
        json = upload_file(request, "")

    json["page"] = "dataset"
    return render(request, 'linearReg/main.html', json)


def edit_table(request):
    json = upload_file(request, request.POST.get('filename'))
    my_list = list(json["my_list"])
    print(my_list[int(request.POST.get('id_edit'))][0])
    if request.POST.get('country_edit') != "":
        country = request.POST.get('country_edit')
    else:
        country = my_list[int(request.POST.get('id_edit'))][0]
    if request.POST.get('Happy_edit') != "":
        hap = request.POST.get('Happy_edit')
    else:
        hap = my_list[int(request.POST.get('id_edit'))][1]
    if request.POST.get('Beer_edit') != "":
        beer = request.POST.get('Beer_edit')
    else:
        beer = my_list[int(request.POST.get('id_edit'))][2]
    one_in_list = (country, hap, beer)
    my_list[int(request.POST.get('id_edit'))] = one_in_list
    json["my_list"] = my_list
    return request
