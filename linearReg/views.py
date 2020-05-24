from django.shortcuts import render
from filesAndUploads.views import upload_file, read_dataset


def open_main(request):
    print(request.session.get("file"))
    json_req = {}

    # Session started
    if request.session.get("start", "yes"):
        json_req["uploaded_file_url"] = "None"

    if request.method == 'POST' and request.POST.get('id_edit') is not None:
        json_req = edit_table(request)
    elif request.method == 'POST' and request.POST.get('sort') is not None:
        json_req = upload_file(request, request.POST.get('sort'))
    elif request.method == 'POST' and request.FILES['my_file']:
        json_req = upload_file(request, "")
    elif request.session.get("start") != "None":
        json_req["uploaded_file_url"] = request.session.get("file")
        filename = json_req["uploaded_file_url"].split('/')[2]
        try:
            country, happiness_score, beer_per_capita = read_dataset(request, filename)
            my_list = zip(country, happiness_score, beer_per_capita)
            json_req["my_list"] = my_list
        except Exception:
            request.session["uploaded_file_url"] = "None"
    
    request.session["file"] = json_req["uploaded_file_url"]
    request.session["start"] = "yes"

    json_req["page"] = "dataset"
    return render(request, 'linearReg/main.html', json_req)


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
    return json
