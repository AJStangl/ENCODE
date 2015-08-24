__author__ = 'AJ'
import requests
def bam_metadata_encode():
    '''
    This script iterates through encode experiments and write out a metadata file for all bam experiments on endcode

    Input: None

    Output: A TXT file (TSV) that contains the metadata for each experiment

    Return: None
    '''
    HEADERS = {'accept': 'application/json'}

    # URL = "https://www.encodeproject.org/search/?searchTerm=%s&type=%s&limit=%s" % ("human", "experiment", "all")
    URL = "https://www.encodeproject.org/search/?searchTerm=human&type=experiment&limit=all"
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
        exp_url.append(base_url + elem)

    '''The above code constructs a list of all urls (exp_url that will be used for data extraction'''

    with open('bam_metadata_encode.txt', 'w') as metadata:
        metadata.write(
            "Name\tExperiment_Name\tDescription\tAssay\tReplicate\tCell_Type\tBio_Sample\tTarget\tAssembly\tLab\tDate"
            "\tVersion\tSource\tDownload_Link\tSource_Link\tSequencer\tRun_Type\tFile_Type\tBiosample_term_id"
            "\tFile_Size\n")

        for elem in exp_url[0:100]:  # Testing Center - Enter number of elements from the exp_url list [X:Y]
            response = requests.get(elem, headers=HEADERS)
            exp_dict = response.json()
            i = 0
            #print len(exp_dict["files"])
            #print exp_dict["files"][i]["file_type"]

            while i < len(exp_dict["files"]):
                if exp_dict["files"][i]["file_type"] == "bam":

                    # Initialize data_dict and data_dict keys if the file format is bam and is aligned to HG19 reference
                    data_dict = {}

                    data_dict.fromkeys(
                        ["Filename", "Name", "Description", "Assay", "Replicate", "Cell_type", "Bio_Sample", "Target",
                         "Assembly", "Lab", "Date", "Version", "Source", "Download_Link", "Source_Link", "Sequencer",
                         "Run_Type", "File_Type", "Biosample_term_id", "File_Size"])

                    # Start Data Extraction
                    ###################################################################################################

                    # Filename
                    data_dict["Filename"] = exp_dict["files"][i]["href"]
                    filename = data_dict["Filename"]
                    temp = filename.split("/")
                    metadata.write(temp[4] + "\t")

                    # Name
                    metadata.write(exp_dict["accession"] + "\t")

                    # Description
                    try:
                        if exp_dict["files"][i]["replicate"]["experiment"]["description"] != "":
                            metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["description"].replace("\n","").replace("\r","") + "\t")
                        else:
                            metadata.write("Not Listed" + "\t")
                    except KeyError:
                        if exp_dict["description"] != "":
                            metadata.write(exp_dict["description"] + "\t")
                        else:
                            metadata.write("Not Listed" + "\t")

                    # Assay
                    try:
                        if exp_dict["files"][i]["replicate"]["experiment"]["assay_term_name"] != "":
                            metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["assay_term_name"] + "\t")
                        else:
                            metadata.write("Not Listed" + "\t")
                    except KeyError:
                        if exp_dict["assay_term_name"] != "":
                            metadata.write(exp_dict["assay_term_name"] + "\t")
                        else:
                            metadata.write("Not Listed" + "\t")

                    # Replicate
                    try:
                        metadata.write(str(exp_dict["files"][i]["replicate"]["biological_replicate_number"]) + "\t")

                    except KeyError:
                        metadata.write("Not Listed" + "\t")

                    # Cell_Type
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["biosample_term_name"] + "\t")
                    except KeyError:
                        metadata.write(exp_dict["biosample_term_name"] + "\t")

                    # Bio_Sample
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["biosample_type"] + "\t")
                    except KeyError:
                        metadata.write(exp_dict["biosample_type"] + "\t")

                    # Target
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["target"]["label"] + "\t")
                    except KeyError:
                        metadata.write("Not Listed" + "\t")

                    # Assembly
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["assembly"][0] + "\t")
                    except (KeyError, IndexError):
                        metadata.write("not listed" + "\t")

                    # Lab
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["lab"]["title"] + "\t")
                    except KeyError:
                        metadata.write(exp_dict["files"][i]["lab"]["title"] + "\t")

                    # Date
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["date_released"] + "\t")
                    except KeyError:
                        metadata.write(exp_dict["files"][i]["date_created"] + "\t")

                    # Version
                    Version = data_dict["Version"] = "1"
                    metadata.write(Version + "\t")

                    # Source
                    metadata.write(exp_dict["award"]["project"] + "\t")

                    # Download_Link
                    metadata.write("https://www.encodeproject.org" + exp_dict["files"][i]["href"] + "\t")

                    # Source_Link
                    metadata.write(elem + "\t")

                    # Sequencer
                    try:
                        metadata.write("Not Listed" + "\t")
                    except KeyError:
                        metadata.write(exp_dict["files"][i]["platform"]["title"] + "\t")

                    # Run_Type
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["run_type"] + "\t")
                    except KeyError:
                        metadata.write("not listed" + "\t")

                    # File_Type
                    metadata.write(exp_dict["files"][i]["file_format"] + "\t")

                    # Biosample_Term_ID
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["biosample_term_id"] + "\t")
                    except KeyError:
                        metadata.write(exp_dict["biosample_term_id"] + "\t")


                    # File_Size
                    fsize = (exp_dict["files"][i]["file_size"]*9.5367431640625e-07)
                    # metadata.write(str(fsize) + "\t")
                    metadata.write(str(fsize))

                    # End of Metadata File Entry
                    metadata.write("\n")

                i = i + 1

    return

bam_metadata_encode()
