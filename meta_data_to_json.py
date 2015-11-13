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


        with open("encode_test.tsv", "r") as infile:
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
                temp = RowObject(int(26117), metadata, source_data, additional_metadata) #, expression_params
                with open("jsons/" + row[0] + ".json", "w") as outfile:
                    outfile.write(json.dumps(temp.__dict__))

            i+= 1
            return


class RowObject:

    '''
    This is a sub-class that creates the fields for the metadata file that will be used in the json object class
    '''

    def __init__(self, gnm_id, metadata, source_data, additional_metadata): #, expression_params
        self.genome_id = gnm_id
        self.source_data = source_data
        self.metadata = metadata
        self.additional_metadata = additional_metadata
        # self.expression_params = expression_params
        return

JsonObject().add_data()