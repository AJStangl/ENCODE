__author__ = 'AJ'
import json, requests
from new_json_encode import RowObject, JsonObject
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



metadata = JsonObject().add_data()
token = get_token()

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

    data = metadata[0]

    url = "https://genomevolution.org/coge/api/v1/experiments?username=%s&token=%s" % (username, token)
    headers = {'Content-type': 'application/json'}
    r = requests.put(url, data, headers=headers)




experiment_add("ajstangl", token, metadata)












