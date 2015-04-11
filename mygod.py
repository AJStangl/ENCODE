__author__ = 'AJ'
import json, csv, os, requests, urllib


class JsonObject:

    def __init__(self):

        with open("bam_metadata_encode.txt", "r") as infile:

            headings = next(infile)
            reader = csv.reader(infile, delimiter='\t')
            i = 0
            for row in reader:

                metadata = [{"link": row[14], "file_type": row[17]}]

                items = [{"path": row[13], "type": "http"}]

                temp = RowObject(row[2], str(25577), metadata, items, row[0], row[12], row[11])

                with open("jsons/" + str(i) + ".json", "w") as outfile:

                    outfile.write(json.dumps(temp.__dict__))
                i += 1


class RowObject:

        def __init__(self, desc, gnm_id, metadata, items, name, source_name, version):
            self.description = desc
            self.genome_id = gnm_id
            self.items = items
            self.metadata = metadata
            self.name = name
            self.source_name = source_name
            self.version = version

def sendJSONObjects():

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    base_url = "http://www.trinnovation.org/temp.php"
    #
    # for file in os.listdir(os.getcwd() + "\jsons"):
    #
    #     tr = ""
    #     with open(os.getcwd() + r'\jsons\\' + file) as jfile:
    #         tr = json.load(jfile)
    #
    #
    #     resp = requests.post(base_url, headers=HEADERS, data=tr)
    #     print resp.status_code

    data = {'value': '7.4', 'decay_time': '300'}
    resp = requests.post(base_url, data=json.dumps(data))
    print resp.status_code

JsonObject()
sendJSONObjects()


