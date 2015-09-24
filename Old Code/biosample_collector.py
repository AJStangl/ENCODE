__author__ = 'AJ'
import requests, json
HEADERS = {'accept': 'application/json'}

def get_sample_url():

    # Currently For RNA Seq Data
    """
    This script will take in a URL from encode and return a list of experiment URLS
    :return: exp_url_list
    """
    base_url = "https://www.encodeproject.org/"
   # search = "search/?type=experiment&assay_term_name=RNA-seq&assembly=hg19&limit=all"
    search = "/search/?type=biosample&organism.scientific_name=Homo+sapiens&status=released"
    url = base_url+search
    r = requests.get(url, headers=HEADERS)
    r = r.json()
    ls = []
    i = 0
    for elem in r:
        if elem == "@graph":


get_sample_url()
