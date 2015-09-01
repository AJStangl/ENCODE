__author__ = 'AJ'
import json, requests


def get_token():
    '''
    This Function Retrieve the access token needed to upload data
    '''
    auth_dict = {}
    with open("config.txt", 'r') as f:
       for line in f:



    #         auth_info[key] = value
    # print auth_info["username"]
    # print auth_info["password"]
    # print auth_info["secret"]
    # print auth_info["key"]





        # payload = {'grant_type':"client_credentials",'username': 'ajstangl', 'password': 'Bio Informatics1', 'scope': 'PRODUCTION'}
        # auth=('mJCMDFPwT6AjKJiuH6Liz3q7gkUa','HSBDwhrJtQqjzYcP_LeHsRPZ508a')
        # r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
        # content_dict=json.loads(r.content)
        # token = content_dict["access_token"]

get_token()

# metadata = JsonObject().add_data()
# def experiment_add(username, token, metadata):
#
#     '''
#     This function will take in a meta data file, iterate through the column in the TSV file and upload experiment
#     to CoGe from ENCODE. It will check for current download state, append a list for successful uploads and failure
#     list.
#
#     :param username: Username for iPlant Account
#     :param token: Token for Requests that is returned from auth_token()
#     :param metadata: List of Json Objects )
#     :return: None
#     '''
#
#     import requests, json
#
#
#
#     url = "https://genomevolution.org/coge/api/v1/experiments?username=%s&token=%s" % (username, token)
#     data = metadata[0]
#     headers = {'Content-type': 'application/json'}
#     r = requests.put(url, data, headers=headers)
#     print r.status_code
#     print data
#
#
# experiment_add("ajstangl", token, metadata)












