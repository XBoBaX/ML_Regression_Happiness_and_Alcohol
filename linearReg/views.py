from django.shortcuts import render
from filesAndUploads.views import upload_file, read_dataset
import numpy as np
import matplotlib.pyplot as plt
from django.conf import settings
from sklearn.metrics import mean_squared_error
from math import sqrt


def mse_calc(actual, prediction):
    expected = [actual]
    predictions = [prediction]
    print(expected, predictions)

    mse = mean_squared_error(expected, predictions)
    return mse


def mrse_calc(actual, prediction):
    rmse = sqrt(mse_calc(actual, prediction))
    return rmse


def computecost(x, y, theta, m):
    a = 1 / (2 * m)
    b = np.sum(((x @ theta) - y) ** 2)
    j = (a) * (b)
    return j


def gradient(x, y, theta, m):
    alpha = 0.00001
    iteration = 2000
    # gradient descend algorithm
    J_history = np.zeros([iteration, 1]);
    for iter in range(0, 2000):
        error = (x @ theta) - y
        temp0 = theta[0] - ((alpha / m) * np.sum(error * x[:, 0]))
        temp1 = theta[1] - ((alpha / m) * np.sum(error * x[:, 1]))
        theta = np.array([temp0, temp1]).reshape(2, 1)
        J_history[iter] = (1 / (2 * m)) * (np.sum(((x @ theta) - y) ** 2))  # compute J value for each iteration
    return theta, J_history


def open_main(request):
    print(request.session.get("file"))
    json_req = {}
    flag_file_get = False

    # Session started
    if request.session.get("start") != "yes":
        json_req["uploaded_file_url"] = "None"

    if request.method == 'POST' and request.POST.get('id_edit') is not None:
        json_req = edit_table(request)
    elif request.method == 'POST' and request.POST.get('actual_value') is not None:
        arg1 = float(request.POST.get('actual_value'))
        arg2 = request.POST.get('expected_value')
        arg2 = float(arg2.replace('[', '').replace(']', ''))
        json_req["mse_value"] = mse_calc(arg1, arg2)
        json_req["mrse_value"] = mrse_calc(arg1, arg2)
        flag_file_get = True
    elif request.method == 'POST' and request.POST.get('sort') is not None:
        json_req = upload_file(request, request.POST.get('sort'))
    elif request.method == 'POST' and request.FILES['my_file']:
        json_req = upload_file(request, "")
    if request.session.get("start") != "None" or flag_file_get == True:
        json_req["uploaded_file_url"] = request.session.get("file")
        filename = json_req["uploaded_file_url"].split('/')[2]
        country, happiness_score, beer_per_capita = read_dataset(request, filename)
        json_req.update(statistics_to_JSON(country, happiness_score, beer_per_capita))


        #DELTE 2 rows leter
        country, happiness_score, beer_per_capita = read_dataset(request, filename)
        json_req.update(line_reg(happiness_score, beer_per_capita, request))
        try:
            country, happiness_score, beer_per_capita = read_dataset(request, filename)
            my_list = zip(country, happiness_score, beer_per_capita)
            json_req.update(statistics_to_JSON(country, happiness_score, beer_per_capita))
            json_req["my_list"] = my_list
            # line_reg(happiness_score,beer_per_capita)
        except Exception:
            print(Exception)
            request.session["uploaded_file_url"] = "None"

    request.session["file"] = json_req["uploaded_file_url"]
    request.session["start"] = "yes"

    json_req["page"] = "dataset"
    return render(request, 'linearReg/main.html', json_req)


def statistics_to_JSON(country, happiness_score, beer_per_capita):
    json_req = {}
    json_req["count_counrt"] = country.size
    json_req["min_HL"] = min(happiness_score)
    json_req["max_HL"] = max(happiness_score)
    json_req["avg_HL"] = round(np.average(happiness_score))
    json_req["min_Beer"] = round(min(beer_per_capita))
    json_req["max_Beer"] = round(max(beer_per_capita))
    json_req["avg_Beer"] = round(np.average(beer_per_capita))
    json_req["median_HL"] = np.median(happiness_score)
    return json_req


def line_reg(HL, BR, request):
    json_ret = {}
    X = HL
    y = BR

    X = X / (np.max(X))
    plt.plot(X, y, 'bo')
    plt.ylabel('Happiness Score')
    plt.xlabel('Alcohol consumption')
    plt.legend(['Happiness Score'])
    plt.title('Alcohol_Vs_Happiness')
    plt.grid()
    plt.savefig(settings.MEDIA_ROOT + '/temp.png')

    json_ret["graph1"] = 'temp.png'

    m = np.size(y)
    X = X.reshape([122, 1])
    x = np.hstack([np.ones_like(X), X])
    theta = np.zeros([2, 1])
    theta, J = gradient(x, y, theta, m)

    plt.plot(X, y, 'bo')
    plt.plot(X, x @ theta, '-')
    plt.axis([0, 1, 3, 7])
    plt.ylabel('Happiness Score')
    plt.xlabel('Alcohol consumption')
    plt.legend(['HAPPY', 'LinearFit'])
    plt.title('Alcohol_Vs_Happiness')
    plt.grid()

    plt.savefig(settings.MEDIA_ROOT + '/temp2.png')

    json_ret["graph2"] = 'temp2.png'

    predict1 = [1, (164 / np.max(HL))] @ theta
    json_ret["pred1"] = predict1

    return json_ret


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
