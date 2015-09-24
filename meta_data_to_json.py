__author__ = 'AJ'
import json, csv
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
        # with open("all_bam_metadata_encode.txt", "r") as infile:
        with open("test_3.txt", "r") as infile: # Change to
            headings = next(infile)
            reader = csv.reader(infile, delimiter='\t')
            i = 0
            data = []

            for row in reader:


                metadata = {"restricted": False, "name": row[0], "description": row[2], "version": row[18], "source_name": row[19]}

                additional_metadata = [{"Date": row[17], "link": row[21], "Assay": row[3],
                                        "Biological Replicate": row[4], "Technical Replicate": row[5],
                                        "Cell Type": row[6], "Health Status": row[7], "Life Stage": row[8],
                                        "Age": row[9], "Sex": row[10], "Bio Sample": row[11], "Target": row[12],
                                        "Assembly": row[13], "Genome Annotation": row[14],
                                        "Output Type": row[15], "Lab": row[16],
                                        "date": row[17], "Source": row[19], "Link": row[21],
                                        "Sequencer": row[22], "Run Type": row[23], "File Type": row[24],
                                        "Biosample ID": row[25]
                                        }]

                source_data = [{"type": "http","path": row[20]}]

                temp = RowObject(int(26119), metadata, source_data, additional_metadata)


                with open("jsons/" + row[0] + ".json", "w") as outfile:
                    data.append(json.dumps(temp.__dict__))
                    outfile.write(json.dumps(temp.__dict__))


            i+= 1

            return data


class RowObject:

    '''
    This is a sub-class that creates the fields for the metadata file that will be used in the json object class
    '''

    def __init__(self, gnm_id, metadata, source_data, additional_metadata):#
        self.genome_id = gnm_id
        self.source_data = source_data
        self.metadata = metadata
        self.additional_metadata = additional_metadata
        return

JsonObject().add_data()