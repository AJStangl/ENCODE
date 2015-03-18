from pip._vendor import requests

__author__ = 'AJ'
def experiment_accession_extractor(searchTerm, Type, Limit):
    HEADERS = {'accept': 'application/json'}
    '''Takes in a search term, for an experiment and returns all URLS that link to the experiment'''
    # URL used to extract the accession ID's for search terms, the type, and how many pages
    # use searchTerm = human, type = experiment, and limit = all
    # Get response to retrieve the JSON element of the web page

    URL = "https://www.encodeproject.org/search/?searchTerm=%s&type=%s&limit=%s" % (searchTerm, Type, Limit)
    response = requests.get(URL, headers=HEADERS)

    encode_dict = response.json()

    '''Interates through the dict json object and extracts the unique experiment URLS'''
    # exp_list contains the /experiment/Accession that is used to access the individual experiments
    exp_list = []
    graph = encode_dict["@graph"]
    for elem in graph:
        for k in elem:
            if elem["@id"] not in exp_list:
                exp_list.append(elem["@id"])

    base_url = "https://www.encode.org"
    exp_url = []
    for elem in exp_list:
        exp_url.append(base_url+elem)

    print exp_url[0]



experiment_accession_extractor("human","experiment", "all")

