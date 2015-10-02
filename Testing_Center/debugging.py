__author__ = 'AJ'
import json, requests, os
i = 0

with open("login.json", "r") as info:
    login = json.load(info)
    info.close()
sub_dir = "C:\Users\AJ\PycharmProjects\Encode\jsons"
json_file_list = os.listdir(sub_dir)
username = login["username"]
password = login["password"]
key = login["key"]
secret = login["secret"]
base_url = "https://geco.iplantcollaborative.org/coge/"
jfile = open(os.path.join(sub_dir, json_file_list[i]), "r")
metadata = jfile.read()
jfile.close()
metadata = json.loads(metadata)
payload = {'grant_type':"client_credentials",'username': username, 'password': password, 'scope': 'PRODUCTION'}
auth = (key, secret)
r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
content_dict = json.loads(r.content)
token = content_dict["access_token"]
# print metadata.keys()
add_meta = metadata["additional_metadata"]

add_dict = {}
for elem in add_meta:
    add_dict[elem['type']] = elem['text']
print add_dict




description = metadata["metadata"]["description"]


# def notebook_add(username, token, base_url, metadata):
#     '''
#
#     :param username: Iplant User ID
#     :param token: Token From Agave API
#     :param base_url: Base URL for API
#     :return: Notebook ID
#     '''
#     class Notebook:
#
#         def __init__(self, nb_name, desc, tp):
#             self.metadata = {"name": nb_name, "description": desc, "restricted": False, "type": tp}
#
#     url = base_url + "api/v1/notebooks/?username=%s&token=%s" % (username, token)
#     mdata = json.loads(metadata)
#     adata = mdata["additional_metadata"]
#
#     for elem in adata:
#         if elem["text"] == "Bio_Sample":
#             nb_name = elem["type"]
#
# # Somethings fucked here
#     desc = mdata["metadata"]["description"]
#     tp = "mixed"
#     pay = json.dumps(vars(Notebook(nb_name, desc, tp)))
#     r = requests.put(url, pay)
#     resp_dict = r.json()
#     return resp_dict


