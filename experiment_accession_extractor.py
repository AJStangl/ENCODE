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
###  END Function ####


exp_url = experiment_accession_extractor("human","experiment", "all")


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

    exp_dict = response.json()

    # print "Accession"+": "+exp_dict["accession"]
    # print "Description"+": "+exp_dict["description"]
    # print "Assay"+": "+exp_dict["assay_term_name"]
    # print "Date"+": "+exp_dict["date_released"]
    # print "Version"+": "+exp_dict["schema_version"]
    # print "Source"+": "+exp_dict["lab"]["title"]
    # print "Link"+": "+"https://www.encodeproject.org"+exp_dict["files"][0]["href"]
    for elem in exp_dict["files"]:
        for k in elem:
            print k












extract_meta(exp_url)











# def generate_meta(dataset):
#     """Generate Metadata TSV File
#
#     A function to generate a TSV metadata file describing experiments contained in a dictionary.
#     Optimized for dictionaries generated with json-decoder.py
#     Current Metadata: Filename*, Name*, Description, Source, Source Link, Sequencer, Health Info
#     "*" Denotes CoGe Required Fields
#
#     Arguments:
#         dataset: Python dictionary with datasets.
#         Dictionary Structure: {huID:[link, health], ...}
#
#      Returns:
#       None - Generates and writes metadata file "meta.txt".
#     """
#     with open('meta.txt', 'w') as metadata:
#         #Write head row
#         metadata.write("Filename\tName\tDescription\tSource\tSource_link\tSequencer\tHealth Records\n")
#         #Iterate through data-set, write each data point meta entry.
#         for key in dataset.keys():
#             meta = generate_item_meta(key, dataset[key][0], dataset[key][1])
#             metadata.write(meta)


