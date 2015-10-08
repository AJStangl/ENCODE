__author__ = 'AJ'
import requests, pprint
def view_exp_url(url):

    HEADERS = {'accept': 'application/json'}
    URL = url
    response = requests.get(url, headers=HEADERS)
    url_dict = response.json()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(url_dict['replicates'])

    print url_dict['replicates'][i]['biological_replicate_number']






view_exp_url("https://www.encodeproject.org/experiments/ENCSR000AAL/")