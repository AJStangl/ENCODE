# __author__ = 'AJ'
import json, requests, os, sys, csv
from threading import Thread
import threading
import Queue
from encode_batch_uploader import file_list,additional_metadata, open_metadata_file, time #check_status, job_fetch,
# from encode_batch_uploader import get_token
from datetime import datetime

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


def get_job(wid, base_url, token):
    url = base_url + "api/v1/jobs/%d/?username=%s&token=%s" % (wid, username, token)
    r = requests.get(url)
    print r
    response_dict = r.json()
    return response_dict


def job_fetch(username, wid, base_url, password, key, secret, thread, token):
    '''
    :param username: the username for auth
    :param token: The token provided from get_token()
    :param wid: The word id provided by experiment_add()
    :return: A JSON (dict) of the response from experiment_fetch
    '''
    while True:
        time.sleep(5)
        url = base_url + "api/v1/jobs/%d/?username=%s&token=%s" % (wid, username, token)
        r = requests.get(url)
        # log_request(thread, r, func_name=job_fetch.__name__)
        if r.status_code == 200:
            time.sleep(5)
            response_dict = r.json()
            print r.content
            if response_dict['status'] == "Running":
                continue
            else:
                return response_dict
        else:
            token = get_token(username, password, key, secret, thread)
            continue

def get_token(username, password, key, secret, thread):
    '''
    This Function Retrieves the access token needed to upload data
    '''
    func_name = get_token.__name__

    while True:
        payload = {'grant_type': "client_credentials", 'username': username, 'password': password, 'scope': 'PRODUCTION'}
        auth = (key, secret)
        r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
        if r.status_code != 200:
            print thread + " Problem With obtaining Token - Sleep and Continue " + str(r._content)
            time.sleep(5)
            continue
        r = r.json()
        return r

def refresh_token(r, key, secret):
    while True:
        auth = (key, secret)
        refresh = r["refresh_token"]
        payload = {'grant_type': 'refresh_token', 'refresh_token': refresh}
        r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
        if r.status_code != 200:
            print thread + " Problem With Refreshing Token - Sleep and Continue"
            time.sleep(5)
            continue
        r = r.json()
        return r



if __name__ == '__main__':
    login = user_data("login.json")
    username = login["username"]
    password = login["password"]
    secret = login["secret"]
    key = login["key"]
    base_url = "https://geco.iplantcollaborative.org/coge/"
    thread = threading.current_thread().name
    # token = get_token(username, password, key, secret, thread)
    wid = 31667
    # comp_dict = get_job(31619, base_url, token)
    while True:
        r = get_token(username, password, key, secret, thread)
        timer = r['expires_in']
        while timer > 14390:
            timer = get_token(username, password, key, secret, thread)['expires_in']
            token = get_token(username, password, key, secret, thread)['access_token']
            print token
            print timer

        if timer < 14390:
            timer = refresh_token(r, key, secret)
            print "refreshing token"
            token = refresh_token(r, key, secret)['access_token']
            print token
            print timer
            continue









    # print job_fetch(username,wid, base_url, password,key,secret,thread, token)



    # exp_name = comp_dict['results'][0]['name'].split(" ")[0]
    # status = comp_dict['status']
    # elapsed = []
    # for elem in comp_dict['tasks']:
    #     if elem['elapsed'] != None:
    #         elapsed.append(elem['elapsed'])
    # elapsed = sum(elapsed)
    # list = [exp_name,comp_dict,elapsed]
    # with open('test.tsv', 'wb') as f:
    #     comp_log = csv.writer(f, lineterminator="\n", delimiter='\t')
    #     comp_log.writerow(list)
    #     f.close()





