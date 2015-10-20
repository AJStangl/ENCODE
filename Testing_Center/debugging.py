# __author__ = 'AJ'
import json, requests, os, sys, csv
from threading import Thread
import threading
import Queue
from encode_batch_uploader import file_list,additional_metadata, open_metadata_file, time #check_status, job_fetch,
from encode_batch_uploader import get_token
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





if __name__ == '__main__':
    login = user_data("login.json")
    username = login["username"]
    password = login["password"]
    secret = login["secret"]
    key = login["key"]
    base_url = "https://geco.iplantcollaborative.org/coge/"
    thread = threading.current_thread().name
    token = get_token(username, password, key, secret, thread)
    wid = 31667
    comp_dict = get_job(31619, base_url, token)


    print job_fetch(username,wid, base_url, password,key,secret,thread, token)



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





