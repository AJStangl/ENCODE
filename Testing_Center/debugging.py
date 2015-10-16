# __author__ = 'AJ'
import json, requests, os, sys
from threading import Thread
import threading
import Queue
from encode_batch_uploader import file_list, check_status, job_fetch, additional_metadata, open_metadata_file, time
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




def test(username, password, key, secret, thread):
    while True:
        payload = {'grant_type': "client_credentials", 'username': username, 'password': password, 'scope': 'PRODUCTION'}
        auth = (key, secret)
        r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
        if r.status_code != 200:
            print thread + " Problem With obtaining Token - Sleep and Continue"
            time.sleep(10)
            continue
        r = r.json()
        refresh = r["refresh_token"]
        payload = {'grant_type': 'refresh_token', 'refresh_token': refresh}
        r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
        if r.status_code != 200:
            print thread + " Problem With Refreshing Token - Sleep and Continue"
            time.sleep(10)
            continue
        r = r.json()
        print thread + " " + test.__name__
        return r['access_token']

def runall():
    thread = threading.current_thread().name
    print thread + " " + runall.__name__
    base_url = "https://geco.iplantcollaborative.org/coge/"
    login = user_data('login.json')
    user = user_data('login.json')
    username = user["username"]
    password = user["password"]
    secret = user["secret"]
    key = user["key"]
    test(username, password, key, secret, thread)



if __name__ == '__main__':

    p1 = Thread(target=runall)
    p2 = Thread(target=runall)
    p3 = Thread(target=runall)
    p4 = Thread(target=runall)

    p1.start()
    p2.start()
    p3.start()
    p4.start()