__author__ = 'AJ'

import json, csv, os, requests, urllib
'''
This script will load "bam_meta_data_encode.txt from the current working directory and create a json files consistent
with the use case of the experiment add RESTful API.
'''



class JsonObject:

    '''
    This class creates the JSON file from the "bam_metadata_encode.txt". It will create a directory called jsons and
    write json files to this path. JSON files are named based on the name of the BAM file.

    It also returns data A lit of json objects
    '''
    def __init__(self):
        return

    def add_data(self):
        # Checks to see if a directory jsons in present and if not creates one
        # d = "jsons/"
        # if not os.path.exists(d):
        #     os.makedirs(d)

        # Opens the metadat file and writes the json object file
        with open("bam_metadata_encode.txt", "r") as infile:

            headings = next(infile)
            reader = csv.reader(infile, delimiter='\t')
            i = 0
            for row in reader:
                data = []
                metadata = [{"link": row[14], "file_type": row[17], "Replicate": row[4], "Target":row[7],
                            "cell_type": row[5], "lab": row[9], "date": row[10], "assembly": row[8],
                            "run_type": row[16], "biosample_term_id": row[18]}]

                source_data = [{"path": row[13], "type": "http"}]

                temp = RowObject(row[2], str(25577), metadata, source_data, row[0], row[12], row[11])

                # with open("jsons/" + row[0] + ".json", "w") as outfile:
                data.append(json.dumps(temp.__dict__))
                    # outfile.write(json.dumps(temp.__dict__))
                i += 1
            return data


class RowObject:
    '''
    This is a sub-class that creates the fields for the metadata file that will be used in the json object class
    '''

    def __init__(self, desc, gnm_id, metadata, source_data, name, source_name, version):
        self.description = desc
        self.genome_id = gnm_id
        self.source_data = source_data
        self.metadata = metadata
        self.name = name
        self.source_name = source_name
        self.version = version
        return


# JsonObject().add_data()







