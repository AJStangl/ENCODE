# __author__ = 'AJ'
import json, requests, os, sys
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

# def bla_token(username, password, key, secret):
#     '''
#     This Function Retrieves the access token needed to upload data
#     '''
#     payload = {'grant_type':"client_credentials",'username': username, 'password': password, 'scope': 'PRODUCTION'}
#     auth = (key, secret)
#     r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
#     r = r.json()
#     refresh = r['refresh_token']
#     payload = {'grant_type': 'refresh_token', 'refresh_token': refresh}
#     auth = (key, secret)
#     r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
#     with open ('test.txt') as f:
    # f.write('request: ' + str(r.request) + '\n')
    # print 'headers: '+ str(r.headers)
    # print 'status code: ' + str(r.status_code)
    # print 'histroy: ' + str(r.history)
    # print 'Url: ' + str(r.url)
    # print 'Reason: ' + str(r.reason)
    # print '_content: ' + str(r._content)
    # print 'elapsed: ' + str(r.elapsed)
    # r = r.json()
    # print 'json: ' + str(r)
    # return r
# def refresh_token(r_token, key, secret, username, password):
#     payload = {'grant_type': 'refresh_token', 'refresh_token':r_token}
#     auth = (key, secret)
#     r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
#     r = r.json()
#     return r


# wid = 31333
# status = job_fetch(username, wid, base_url, login)

# base_url = "https://geco.iplantcollaborative.org/coge/"
# login = user_data('login.json')
# user = user_data('login.json')
# username = user["username"]
# password = user["password"]
# secret = user["secret"]
# key = user["key"]

# key = bla_token(username,password,key,secret)

def hell():
    print sys._getframe().f_code.co_name


hell()



