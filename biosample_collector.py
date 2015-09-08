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
    search = "/search/?type=biosample&organism.scientific_name=Homo+sapiens&limit=all&status=released"
    url = base_url+search
    r = requests.get(url, headers=HEADERS)

    encode_dict = r.json()

    exp_list = [] # contains end point
    exp_url_list = [] # contains full URL for experiment

    print encode_dict
    # for elem in encode_dict["@graph"]:
    #     for k in elem:
    #         if elem["@id"] not in exp_list:
    #             exp_list.append(elem["@id"])

    # for elem in exp_list:
    #     exp_url_list.append(base_url + elem)
    #
    # print exp_url_list

get_sample_url()
