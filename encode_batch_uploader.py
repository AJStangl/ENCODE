__author__ = 'AJ'
import json, requests, os
from meta_data_to_json import RowObject, JsonObject
def get_token():
    '''
    This Function Retrieves the access token needed to upload data
    '''
    payload = {'grant_type':"client_credentials",'username': 'ajstangl', 'password': 'Bio Informatics1', 'scope': 'PRODUCTION'}
    auth = ('mJCMDFPwT6AjKJiuH6Liz3q7gkUa', 'HSBDwhrJtQqjzYcP_LeHsRPZ508a')
    r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
    content_dict = json.loads(r.content)
    token = content_dict["access_token"]
    return token

def experiment_add(username, token, metadata):

    '''
    This function will take in a meta data file, iterate through the column in the TSV file and upload experiment
    to CoGe from ENCODE. It will check for current download state, append a list for successful uploads and failure
    list.

    :param username: Username for iPlant Account
    :param token: Token for Requests that is returned from auth_token()
    :param metadata: List of Json Objects )
    :return: None
    '''

    data = metadata

    url = "https://geco.iplantcollaborative.org/coge/api/v1/experiments?username=%s&token=%s" % (username, token)
    # url = "https://genomevolution.org/coge/api/v1/experiments?username=%s&token=%s" % (username, token) # Used for Production
    headers = {'Content-type': 'application/json'}
    r = requests.put(url, data, headers=headers)
    rep_dict =  r.json()
    return rep_dict

def job_fetch(username, token, wid):
    '''
    :param username: the username for auth
    :param token: The token provided from get_token()
    :param wid: The word id provided by experiment_add()
    :return: A JSON (dict) of the response from experiment_fetch
    '''
    url = "https://geco.iplantcollaborative.org/coge/api/v1/jobs/%d/?username=%s&token=%s" % (wid, username, token)
    r = requests.get(url)
    comp_dict = r.json()
    while comp_dict["status"] != "complete":
        r = requests.get(url)
        comp_dict = r.json()
        if comp_dict["status"] == "failed":
            with open("error_log.txt", "a") as error_log:
                error_log.write(comp_dict)


    return comp_dict

def open_metadata_file(i):
    '''

    :param i:An interger that
    :return:Metadata string in JSON format
    '''
    sub_dir = "C:\Users\AJ\PycharmProjects\Encode\jsons"
    json_file_list = os.listdir(sub_dir)
    file = open(os.path.join(sub_dir, json_file_list[i]), "r")
    metadata = file.read()
    file.close()
    return metadata




# Sudo Main
username = "ajstangl"
token = get_token()
metadata = open_metadata_file(0)
response = experiment_add(username, token, metadata)
wid = response["id"]
success = response["success"]
temp = json.dumps(job_fetch(username, token, wid))
print temp
























