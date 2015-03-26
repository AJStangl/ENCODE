from pip._vendor import requests
__author__ = 'AJ'

def experiment_accession_extractor(searchTerm, Type, Limit):
    """
    Generates a list of experiment URLs from https://www.encode.org related to the input search query

    Argument(s):

    searchTERM: Search for a specific term in encode (use 'human' as default)

    Type: Additional search paramter used to filter results (use 'experiment' as default)

    Limit: Limit the number of pages to search (use 'all' as default)

    Returns: A list of all experimental URLS used to access the data in encode (exp_url)

    """

    HEADERS = {'accept': 'application/json'}

    URL = "https://www.encodeproject.org/search/?searchTerm=%s&type=%s&limit=%s" % (searchTerm, Type, Limit)

    response = requests.get(URL, headers=HEADERS)

    #  Dict for json object obtained from ENCODE
    encode_dict = response.json()

    #  List of experiment URLS that will be returned by this function
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
    """
    Generates a TSV file for the metadat fields Filename, Name, Description, Lab, Date_Created, Source,
    Source Link Sequencer, Run Type, and File Type

    Argument(s):

    exp_url: A URL List generated from experiment_accession_extractor that contains the direct URL for each experiment.

    Returns: NONE

    Writes: A TSV File with all of the metadata fields listed above
    """

    #  Opens the tsv file to write metadata to
    with open('experiment_metadata.tsv', 'w') as metadata:

        metadata.write("Filename\tName\tDescription\tLab\tAssay\tCell_Type\tBiosample\tTarget_Gene\tDate_Created\tSource\tSource_Link\tSequencer\tRun_Type\tFiletype\n")

        # for each experiment accession
        for elem in exp_url:  # Testing Center
            HEADERS = {'accept': 'application/json'}
            URL = elem
            response = requests.get(URL, headers=HEADERS)

            #  The JSON object in dict format for data extraction
            exp_dict = response.json()

            # For each file in the primary accession, write it to the tsv
            i = 0

            while i < len(exp_dict["files"]):

                # Only returns the fastq file data formats
                if exp_dict["files"][i]["file_format"] == "fastq":

                    #  Initialize the dict to store metadata
                    data_dict = {}

                    # Populate the dict with Keys that will be placed into the TSV File
                    data_dict.fromkeys(["Filename", "Name", "Description", "Lab", "Assay", "Cell_Type", "Biosample", "Target_Gene", "Date_Created", "Source","Source_Link", "Sequencer", "Run_Type", "Filetype"])

                    # Get the filename and strip the '/'s from the key ["files"][i]["href"]
                    data_dict["Filename"] = exp_dict["files"][i]["href"]
                    filename = data_dict["Filename"]
                    temp = filename.split("/")

                    # Write exp_dict values to metadata file
                    metadata.write(temp[4] + "\t")                                                        # Filename
                    metadata.write(exp_dict["accession"] + "\t")                                          # Name
                    # metadata.write(exp_dict["description"] + "\t")
                    metadata.write(exp_dict["description"] + "\t")  #  Description
                    metadata.write(exp_dict["lab"]["title"] + "\t") # Lab

                    if "replicate" in exp_dict["files"][i]:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["assay_term_name"] + "\t")    # Assay
                    else:
                        metadata.write("Not Avail" + "\t")

                    # Check if the platform key/value pair exists in exp_dict and write it to the tsv
                    if "biosample_type" in exp_dict:
                        metadata.write(exp_dict["biosample_type"] + "\t")                                  # Cell_Type
                    else:
                        metadata.write("unknown\t")                                                        # Cell_Type

                    if "biosample_term_name" in exp_dict:
                        metadata.write(exp_dict["biosample_term_name"] + "\t")# Biosample
                    else:
                        metadata.write("unknown" + "\t")

                    if "replicate" in exp_dict["files"][i] and "target" in exp_dict["files"][i]["replicate"]["experiment"]:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["target"]["name"] + "\t") # Target_Gene
                    else:
                        metadata.write("Not Avail" + "\t")


                    metadata.write(exp_dict["files"][i]["date_created"] + "\t")                            # Date Created
                    metadata.write(exp_dict["award"]["project"] + "\t")                                    # Source
                    metadata.write("https://www.encodeproject.org"+exp_dict["files"][i]["href"] + "\t")    # Source Link

                    # Check if the platform key/value pair exists in exp_dict and write it to the tsv
                    if "platform" in exp_dict["files"][i]:
                        metadata.write(exp_dict["files"][i]["platform"]["title"] + "\t")                   # Sequencer
                    else:
                        metadata.write("unknown" + "\t")                                                   # Sequencer
                    if "run_type" in exp_dict:
                        metadata.write(exp_dict["run_type"] + "\t")                                        # Run Type
                    else:
                        metadata.write("unknown" + "\t")                                                        # Run Type
                    metadata.write(exp_dict["files"][i]["file_format"] + "\t")                             # File Type


                    metadata.write("\n")
                i = i + 1








# Pspeudo Main

exp_url = experiment_accession_extractor("human","experiment", "all") # For all human experiments
extract_meta(exp_url)














