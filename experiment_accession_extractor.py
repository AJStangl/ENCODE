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

    base_url = "https://www.encodeproject.org"
    exp_url = []
    for elem in exp_list:
        exp_url.append(base_url+elem)


    return exp_url

def extract_meta(exp_url):

    with open('experiment_metadata.tsv', 'w') as metadata:
        metadata.write("Filename\tName\tDescription\tLab\tBiosample\tDate_Created\tSource\tSource_Link\tSequencer\tRun_Type\tFiletype\n")  #"Filename\tName\tDescription\tDate_Created\tBiosample\tSource\tSource_Link\tSequencer\tFiletype\tBiosample\n"
        # for each experiment accession
        for elem in exp_url[0:2]:  # Testing Center
            HEADERS = {'accept': 'application/json'}
            URL = elem
            response = requests.get(URL, headers=HEADERS)
            exp_dict = response.json()

            # For each file in the primary accession, write it to the tsv
            i = 0
            while i < len(exp_dict["files"]):

                if exp_dict["files"][i]["file_format"] == "fastq":  # Only returns the fastq file data formats
                    data_dict = {}
                    data_dict.fromkeys(["Filename", "Name", "Description", "Lab", "Date_Created", "Biosample", "Source","Source_Link", "Sequencer", "Run_Type", "Filetype"])
                    data_dict["Filename"] = exp_dict["files"][i]["href"]

                    # Get the filename and strip the '/'s from it
                    filename = data_dict["Filename"]
                    temp = filename.split("/")
                    # Write exp_dict values to metadata file
                    metadata.write(temp[4] + "\t")  # Filename
                    metadata.write(exp_dict["accession"] + "\t")  # Name
                    metadata.write(exp_dict["description"] + "\t")  # Description
                    metadata.write(exp_dict["lab"]["title"] + "\t")  # Lab

                    # Check if the platform key/value pair exists in exp_dict and write it to the tsv
                    if "biosample_type" in exp_dict:
                        metadata.write(exp_dict["biosample_type"]+" : "+exp_dict["biosample_term_name"] + "\t")  #Biosample
                    else:
                        metadata.write("unknown\t")  # Biosample
                    metadata.write(exp_dict["files"][i]["date_created"] + "\t")  # Date Created
                    metadata.write(exp_dict["award"]["project"] + "\t")  # Source
                    print exp_dict["award"]["project"]
                    # Add Lab field for meta data
                    metadata.write("https://www.encodeproject.org"+exp_dict["files"][i]["href"] + "\t")  # Source Link

                    # Check if the platform key/value pair exists in exp_dict and write it to the tsv
                    if "platform" in exp_dict["files"][i]:
                        metadata.write(exp_dict["files"][i]["platform"]["title"] + "\t")  # Sequencer
                    else:
                        metadata.write("none\t") # Sequencer
                    if "run_type" in exp_dict:
                        metadata.write(exp_dict["run_type"] + "\t")  # Run Type
                    else:
                        metadata.write("none\t") # Run Type
                    metadata.write(exp_dict["files"][i]["file_format"] + "\t")  # File Type


                    metadata.write("\n")
                i = i + 1








# Pseudo Main

exp_url = experiment_accession_extractor("human","experiment", "all") # For all human experiments
extract_meta(exp_url)














