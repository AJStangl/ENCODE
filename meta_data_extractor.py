__author__ = 'AJ'
import requests, json, os, sys, csv

def get_exp_url(search):
    """
    :param search: The endpoint url for searching encode.
    This script will take in a URL from encode and return a list of experiment URLS
    :return: exp_url_list
    """
    HEADERS = {'accept': 'application/json'}
    base_url = "https://www.encodeproject.org/"
    url = base_url+search
    r = requests.get(url, headers=HEADERS)
    encode_dict = r.json()
    exp_list = [] # contains end point
    exp_url_list = [] # contains full URL for experiment

    for elem in encode_dict["@graph"]:
        for k in elem:
            if elem["@id"] not in exp_list:
                exp_list.append(elem["@id"])

    for elem in exp_list:
        exp_url_list.append(base_url + elem)

    return exp_url_list


def metadata_extractor(exp_url_list, filename):
    """
    Extracts metadata and URLs for meta_data_json.py and export the data as a TSV
    :param exp_url_list: URL list from get_exp_url.py
    :param filename: Filename of TSV
    :return: NONE
    """
    HEADERS = {'accept': 'application/json'}
    with open(filename + '.tsv', 'w') as metadata:
        metadata.write(
            "Name\tExperiment_Name\tDescription\tAssay\tBiological_Replicate\tTechnical_Replicate\t"
            "Cell_Type\tHealth_Status\tLife_Stage\tAge\tSex\tBio_Sample\tTarget\tAssembly\tGenome_Annotation"
            "\tOutput_Type\tLab\tDate"
            "\tVersion\tSource\tDownload_Link\tSource_Link\tSequencer\tRun_Type\tFile_Type\tBiosample_term_id"
            "\tFile_Size\n")

        for elem in exp_url_list:
            response = requests.get(elem, headers=HEADERS)
            exp_dict = response.json()

            i = 0

            while i < len(exp_dict["files"]): # Checks to see if annotation is present
                if exp_dict["files"][i]["file_type"] == "bam":

                    # Start Data Extraction
                    ###################################################################################################

                    # Filename
                    metadata.write(exp_dict["files"][i]["accession"] + "\t")

                    # Exp_Name
                    metadata.write(exp_dict["accession"] + "\t")

                    # Description
                    try:
                        if exp_dict["files"][i]["replicate"]["experiment"]["description"] != "":
                            metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["description"].replace("\n","").replace("\r","") + "\t")
                        else:
                            metadata.write("not listed" + "\t")
                    except KeyError:
                        if exp_dict["description"] != "":
                            metadata.write(exp_dict["description"] + "\t")
                        else:
                            metadata.write("not listed" + "\t")

                    # Assay
                    try:
                        if exp_dict["files"][i]["replicate"]["experiment"]["assay_term_name"] != "":
                            metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["assay_term_name"] + "\t")
                        else:
                            metadata.write("not listed" + "\t")
                    except KeyError:
                        if exp_dict["assay_term_name"] != "":
                            metadata.write(exp_dict["assay_term_name"] + "\t")
                        else:
                            metadata.write("not listed" + "\t")

                    # Biological Replicate
                    try:
                        metadata.write(str(exp_dict["files"][i]["replicate"]["biological_replicate_number"]) + "\t")

                    except KeyError:
                        metadata.write("not listed" + "\t")

                    # Technical Replicate
                    try:
                        metadata.write(str(exp_dict["files"][i]["replicate"]["technical_replicate_number"]) + "\t")
                    except KeyError:
                        metadata.write("not listed" + "\t")

                    # Cell_Type
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["biosample_term_name"] + "\t")
                    except KeyError:
                        metadata.write(exp_dict["biosample_term_name"] + "\t")

                    # Health
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["library"]["biosample"]["health_status"] + "\t")
                    except KeyError:
                        metadata.write("not listed" + "\t")
                    # Life Stage
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["library"]["biosample"]["life_stage"] + "\t")
                    except KeyError:
                        metadata.write("not listed" + "\t")
                    # Age
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["library"]["biosample"]["age"] + "\t")
                    except KeyError:
                        metadata.write("not listed" + "\t")
                    # Sex
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["library"]["biosample"]["sex"] + "\t")
                    except KeyError:
                        metadata.write("not listed" + "\t")

                    # Bio_Sample
                    try:
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["biosample_type"] + "\t")
                    except KeyError:
                        metadata.write(exp_dict["biosample_type"] + "\t")

                    # Target
                    try:
                        metadata.write(exp_dict["target"]["label"] + "\t")
                    except KeyError:
                        metadata.write("not listed" + "\t")

                    # Assembly
                    try:
                        metadata.write(exp_dict["files"][i]["assembly"] + "\t")
                    except KeyError:
                        metadata.write("not listed" + "\t")

                    # Genome Annotation
                    try:
                        metadata.write(exp_dict["files"][i]["genome_annotation"] + "\t")
                    except (KeyError, IndexError):
                        metadata.write("not listed" + "\t")

                    #output_type
                    try:
                        metadata.write(exp_dict["files"][i]["output_type"] + "\t")

                    except (KeyError,IndexError):
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
                    Version = str(1)
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
                        metadata.write(exp_dict["files"][i]["run_type"] + "\t")
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
                    metadata.write(str(fsize))
                    metadata.write("\n")

                i += 1
    return

class JsonObject:

    '''
    This class creates the JSON file from the "bam_metadata_encode.txt". It will create a directory called jsons and
    write json files to this path. JSON files are named based on the name of the BAM file.

    It also returns data A lit of json objects
    '''
    def __init__(self):
        return

    def add_data(self, in_file):


        with open(in_file, "r") as infile:
            headings = next(infile)
            reader = csv.reader(infile, delimiter='\t')
            i = 0
            for row in reader:
                metadata = {"restricted": False, "name": row[0], "description": row[2], "version": row[18],
                            "source": "Encode"}
                additional_metadata = [{"type": "Cell Type", "text": row[6]},
                                       {"type": "Biological Replicate", "text": row[4]},
                                       {"type": "Technical Replicate", "text": row[5]},
                                       {"type": "Health Status", "text": row[7]},
                                       {"type": "Life Stage", "text": row[8]},
                                       {"type": "Age", "text": row[9]},
                                       {"type": "Sex", "text": row[10]},
                                       {"type": "Biosample", "text": row[11]},
                                       {"type": "Assay Target", "text": row[12]},
                                       {"type": "Genome Assembly", "text": row[13]},
                                       {"type": "Output Type ", "text": row[15]},
                                       {"type": "Lab Info", "text": row[16]},
                                       {"type": "Date", "text": row[17]},
                                       {"type": "Experiment URL", "text": row[21]},
                                       {"type": "Sequencer Info", "text": row[22]},
                                       {"type": "Sequencer Run Info", "text": row[23]},
                                       {"type": "File Type", "text": row[24]},
                                       {"type": "Encode Biosample ID", "text": row[25]},
                                       {"type": "File Size", "text": row[26]},
                                       {"type": "Experiment Name", "text": row[1]}]

                expression_params = {"-Q": 20}
                source_data = [{"type": "http", "path": row[20]}]
                temp = RowObject(int(26225), metadata, source_data, additional_metadata, expression_params)
                with open("jsons/" + row[0] + ".json", "w") as outfile:
                    outfile.write(json.dumps(temp.__dict__))

            i+= 1
            return


class RowObject:

    '''
    This is a sub-class that creates the fields for the metadata file that will be used in the json object class
    '''

    def __init__(self, gnm_id, metadata, source_data, additional_metadata, expression_params):
        self.genome_id = gnm_id
        self.source_data = source_data
        self.metadata = metadata
        self.additional_metadata = additional_metadata
        self.expression_params = expression_params
        return
if __name__ == '__main__':
    search = sys.argv[1]
    filename = sys.argv[2]
    in_file = filename + ".tsv"
    exp_url_list = get_exp_url(sys.argv[1])
    # exp_url_list = get_exp_url(search= "/search/?type=experiment&assay_term_name=ChIP-seq&status=released&assembly=hg19&limit=all")
    metadata_extractor(exp_url_list, filename)
    JsonObject().add_data(in_file)


