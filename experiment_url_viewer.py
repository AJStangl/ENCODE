__author__ = 'AJ'
import requests
def view_exp_url(url):

    HEADERS = {'accept': 'application/json'}
    URL = url
    response = requests.get(url, headers=HEADERS)
    url_dict = response.json()

    print url_dict







view_exp_url("https://www.encodeproject.org/experiments/ENCSR369RVN/")