from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np


def upload_file(request, url):
    if url == "":
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
    else:
        filename = url.split('/')[2]
        uploaded_file_url = url
    country, happiness_score, beer_per_capita = read_dataset(request, filename)
    mylist = zip(country, happiness_score, beer_per_capita)
    return {"uploaded_file_url": uploaded_file_url, 'mylist': mylist}


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