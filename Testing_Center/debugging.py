__author__ = 'AJ'
import json, requests, os
from encode_batch_uploader import notebook_search,get_token, open_metadata_file, user_data, file_list, primary_metadata, additional_metadata, notebook_add
sub_dir = "C:\Users\AJ\PycharmProjects\Encode\Test J"
login = user_data("login.json")
username = login["username"]
base_url = "https://geco.iplantcollaborative.org/coge/"
json_file_list = file_list(sub_dir)
num = [0,1,2,3,4,5,6,7,8,9,10]
i = 0
token = get_token(username, password=login["password"], key=login["key"], secret=login["secret"])
metadata = open_metadata_file(i, sub_dir, json_file_list)
pri_meta = primary_metadata(metadata)
add_meta = additional_metadata(metadata)
term = add_meta["Encode Biosample ID"]
nb_check = notebook_search(term, base_url, username, token)
print notebook_search(term, base_url, username, token)
# print notebook_add(add_meta,username, token, base_url)


