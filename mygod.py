__author__ = 'AJ'
import json, csv, pprint


'''['Name', 'Experiment_Name', 'Description', 'Assay', 'Replicate', 'Cell_Type', 'Bio_Sample', 'Target', 'Assembly',
'Lab', 'Date', 'Version', 'Source', 'Download_Link', 'Source_Link', 'Sequencer', 'Run_Type', 'File_Type',
'Biosample_term_id', 'File_Size']'''

class Fields:

    def __init__(self, genome_id, version, description, name, source):
        self.genome_id = genome_id
        self.version = version
        self.source = source
        self.description = description
        self.name = name

class metadata:
    def __init__(self, ):
        self.metadata = metadata



with open("bam_metadata_encode.txt", "r") as infile:
    headings = next(infile)
    headings = headings.replace('\n', '')
    headings = headings.split("\t")


    reader = csv.reader(infile, delimiter='\t')
    row_count = len(list(reader))
    ite = 0
    infile.seek(0)
    exp_list= []

    for headings in reader:
        ite += 1

        exp_list.append(Fields(25577, headings[11], headings[2], headings[0], headings[12]))

#
jsfile = file('test.json', 'w')
i = 1
while i < len(exp_list):
    jsfile.write(json.dumps(exp_list[1].__dict__))

    i = i + 1
jsfile.close()





