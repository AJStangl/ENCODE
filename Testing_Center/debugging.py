# __author__ = 'AJ'
import json, requests, os, sys, csv
from threading import Thread
import threading
import Queue
from encode_batch_uploader import file_list, check_status, job_fetch, additional_metadata, open_metadata_file, time
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






if __name__ == '__main__':
    login = user_data("login.json")
    username = login["username"]
    password = login["password"]
    secret = login["secret"]
    key = login["key"]
    base_url = "https://geco.iplantcollaborative.org/coge/"
    thread = threading.current_thread().name
    token = get_token(username, password, key, secret, thread)
    comp_dict = get_job(31619, base_url, token)

    exp_name = comp_dict['results'][0]['name'].split(" ")[0]
    status = comp_dict['status']
    elapsed = []
    for elem in comp_dict['tasks']:
        if elem['elapsed'] != None:
            elapsed.append(elem['elapsed'])
    elapsed = sum(elapsed)
    list = [exp_name,comp_dict,elapsed]
    with open('test.tsv', 'wb') as f:
        comp_log = csv.writer(f, lineterminator="\n", delimiter='\t')
        comp_log.writerow(list)
        f.close()





