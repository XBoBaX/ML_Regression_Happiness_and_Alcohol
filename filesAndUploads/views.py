from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np


def upload_file(request, url):
    if url == "":
        my_file = request.FILES['my_file']
        fs = FileSystemStorage()
        filename = fs.save(my_file.name, my_file)
        uploaded_file_url = fs.url(filename)
    else:
        filename = url.split('/')[2]
        uploaded_file_url = url

    country, happiness_score, beer_per_capita = read_dataset(request, filename)
    my_list = zip(country, happiness_score, beer_per_capita)
    return {"uploaded_file_url": uploaded_file_url, 'my_list': my_list}


def read_dataset(request, url_file):
    data = pd.read_csv('media/' + url_file, ',', usecols=['Country', 'Beer_PerCapita', 'HappinessScore'])
    A = data[['Beer_PerCapita', 'HappinessScore']]
    B = data[['Country']]
    matrix = np.array(A.values, 'float')
    matrix2 = np.array(B.values, 'object_')

    country = matrix2[:, 0]
    happiness_score = matrix[:, 0]
    beer_per_capita = matrix[:, 1]
    return country, happiness_score, beer_per_capita

