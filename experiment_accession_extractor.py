from pip._vendor import requests

__author__ = 'AJ'
def experiment_accession_extractor(searchTerm, Type, Limit):
    """Generate List of Experimental URLs from https://www.encode.org

    A function to generate a list of all experiments found in encode that is used as an input to extract relavent
    metadata fields for CoGe

    Arguments:
    searchTERM: Search for a specific term in encode (use 'human' as default)
    Type: Additional search paramter used to filter results (use 'experiment' as default)
    Limit: Limit the number of pages to search (use 'all' as default)

    Returns: A list of all experimental URLS used to access the data in encode (exp_url)
    """
    HEADERS = {'accept': 'application/json'}

    URL = "https://www.encodeproject.org/search/?searchTerm=%s&type=%s&limit=%s" % (searchTerm, Type, Limit)

    response = requests.get(URL, headers=HEADERS)

    encode_dict = response.json()

    exp_list = []

    graph = encode_dict["@graph"]

    for elem in graph:
        for k in elem:
            if elem["@id"] not in exp_list:
                exp_list.append(elem["@id"])

    base_url = "https://www.encodeproject.org/"
    exp_url = []
    for elem in exp_list:
        exp_url.append(base_url+elem)




    return exp_url[0]






def extract_meta(exp_url):
    """Extracts the meta data fields: Filename*, Name*, Description, Source, Source Link, Sequencer, Health Info

    A function to generate a list of all experiments found in encode that is used as an input to extract relavent
    metadata fields for CoGe

    Arguments:
    exp_url: The experiment URL that contains the information for the experiment

    Returns: A dict object containing Filename, Name, Decription, Source, Source Link, Platform, biosample
    """
    HEADERS = {'accept': 'application/json'}

    URL = exp_url

    response = requests.get(URL, headers=HEADERS)

    '''Contains informations on priimarn id'''
    exp_dict = response.json()

    '''Contains information on relevent experiments'''

    file_list = exp_dict["files"]
    file_acc = []
    href = []

    for elem in file_list:
        file_acc.append(elem["accession"])
        href.append(elem["href"])



    print file_acc
    




# Pseudo Main

exp_url = experiment_accession_extractor("human","experiment", "all") # For all human experiments
extract_meta(exp_url)














