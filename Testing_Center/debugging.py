# __author__ = 'AJ'
import json, requests
def user_data(mfile):
    '''
    This function will return the user data for login
    :param file: TSV file with login information
    :return: Dict of Login Information
    '''
    login = {}
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


user = user_data('login.json')
username = user["username"]
password = user["password"]
secret = user["secret"]
key = user["key"]

while True:
    token_dict = get_token(username,password,key,secret)
    print token_dict
    token = token_dict['access_token']
    r_token = token_dict['refresh_token']
    print token
    r_dict = refresh_token(r_token,key,secret,username,password)
    print r_dict
    print r_dict['access_token']





