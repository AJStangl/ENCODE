__author__ = 'AJ'
import json, requests, os, timeit, csv
from encode_batch_uploader import notebook_search,get_token, open_metadata_file, user_data,\
    file_list, primary_metadata, additional_metadata, notebook_add, check_status, job_fetch

start_time = timeit.default_timer()
sub_dir = 'C:\Users\AJ\PycharmProjects\Encode\jsons'
login = user_data("login.json")
username = login["username"]
base_url = "https://geco.iplantcollaborative.org/coge/"
json_file_list = file_list(sub_dir)
i = 0
token = get_token(username, password=login["password"], key=login["key"], secret=login["secret"])
metadata = open_metadata_file(i, sub_dir, json_file_list)
pri_meta = primary_metadata(metadata)
add_meta = additional_metadata(metadata)
term = add_meta["Encode Biosample ID"]
nb_check = notebook_search(term, base_url, username, token)
nb_id = notebook_search(term, base_url, username, token)['id']

wid = 31244
status = check_status(username,token,wid,0,base_url)
comp_dict = job_fetch(username, token, wid, base_url)
exp_name = pri_meta["name"]
elapsed = timeit.default_timer() - start_time

test = []

comp_dict = json.dumps(comp_dict)


l = [exp_name, wid, status, comp_dict, elapsed]
test.append(l)

with open("test.tsv", "wb") as out:
    writer = csv.writer(out, lineterminator="\n", delimiter='\t')
    for elem in test:
        writer.writerow(elem)
    out.close()






