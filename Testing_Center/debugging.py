# __author__ = 'AJ'
import json, requests, os
from encode_batch_uploader import file_list, check_status, job_fetch, additional_metadata, open_metadata_file
def user_data(mfile):
    '''

    This function will return the user data for login
    :param file: TSV file with login information
    :return: Dict of Login Information
    '''

    with open(mfile, "r") as info:
        login = json.load(info)
        info.close()
    return login

def get_token(username, password, key, secret):
    '''
    This Function Retrieves the access token needed to upload data
    '''
    payload = {'grant_type':"client_credentials",'username': username, 'password': password, 'scope': 'PRODUCTION'}
    auth = (key, secret)
    r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
    r = r.json()
    return r

def refresh_token(r_token, key, secret, username, password):
    payload = {'grant_type': 'refresh_token', 'refresh_token':r_token}
    auth = (key, secret)
    r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
    r = r.json()
    return r

# base_url = "https://geco.iplantcollaborative.org/coge/"
# login = user_data('login.json')
# user = user_data('login.json')
# username = user["username"]
# password = user["password"]
# secret = user["secret"]
# key = user["key"]
# wid = 31333
# status = job_fetch(username, wid, base_url, login)
# print status


# while True:
#     token_dict = get_token(username,password,key,secret)
#     print token_dict
#     token = token_dict['access_token']
#     r_token = token_dict['refresh_token']
#     print token
#     r_dict = refresh_token(r_token,key,secret,username,password)
#     print r_dict
#     print r_dict['access_token']

sub_dir = 'C:\Users\AJ\PycharmProjects\Encode\json'
json_file_list = file_list(sub_dir)
# max_files = len(json_file_list)
#
# i = 0
# while i < max_files:
#     print json_file_list[i]
#     print i
#     os.remove(sub_dir + "/"+ json_file_list[i])
#     i = i + 1

metadata = open_metadata_file([0], sub_dir, json_file_list)


add_meta = additional_metadata(metadata)
print add_meta

