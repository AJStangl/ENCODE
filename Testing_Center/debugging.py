__author__ = 'AJ'
import json, csv, os, requests, urllib, time
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

def job_fetch(username, wid, base_url, token):
    '''
    :param username: the username for auth
    :param token: The token provided from get_token()
    :param wid: The word id provided by experiment_add()
    :return: A JSON (dict) of the response from experiment_fetch
    '''
    url = base_url + "api/v1/jobs/%d/?username=%s&token=%s" % (wid, username, token)
    r = requests.get(url)
    response_dict = r.json()
    return response_dict

def get_token(username, password, key, secret):
    '''
    This Function Retrieves the access token needed to upload data
    '''
    func_name = get_token.__name__
    while True:
        payload = {'grant_type': "client_credentials", 'username': username, 'password': password, 'scope': 'PRODUCTION'}
        auth = (key, secret)
        r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
        print r.content
        time.sleep(1)
        if r.status_code != 200:
            time.sleep(30)
            continue
        r = r.json()
        refresh = r["refresh_token"]
        payload = {'grant_type': 'refresh_token', 'refresh_token': refresh}
        r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
        print r.content
        if r.status_code != 200:
            time.sleep(30)
            continue
        r = r.json()
        return r['access_token']

# def test_write(wid, token):
#     data_dict = {}
#     with open('test.txt' , 'ab') as f:


if __name__ == '__main__':
    user = user_data('login.json')
    username = user["username"]
    password = user["password"]
    secret = user["secret"]
    key = user["key"]
    base_url = "https://geco.iplantcollaborative.org/coge/"
    token = get_token(username, password, key, secret)
    job = job_fetch(username, 32470, base_url, token)
    data = {}
    data[token] = job['id']
    data = json.dumps(data)
    print data
