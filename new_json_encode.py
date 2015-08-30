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
        # Opens the metadata file and writes the json object file
        with open("bam_metadata_encode.txt", "r") as infile:

            headings = next(infile)
            reader = csv.reader(infile, delimiter='\t')
            i = 0
            for row in reader:
                data = []
                '''need to fix to pull from meta data tsv'''


                metadata = {"restricted": True, "name": row[0], "description": row[2], "version": row[11],
                            "source_name": "Encode"}

                additional_metadata = [{"Date": row[10], "link": row[14]}]


                source_data = [{"type": "http","path": row[13]}]

                temp = RowObject(int(25577), metadata, source_data, additional_metadata)

                with open("jsons/" + row[0] + ".json", "w") as outfile:
                    data.append(json.dumps(temp.__dict__))
                    outfile.write(json.dumps(temp.__dict__))
                i += 1
            return data


class RowObject:
    '''
    This is a sub-class that creates the fields for the metadata file that will be used in the json object class
    '''

    def __init__(self, gnm_id, metadata, source_data, additional_metadata):
        self.genome_id = gnm_id
        self.source_data = source_data
        self.metadata = metadata
        self.additional_metadata = additional_metadata
        return


JsonObject().add_data()