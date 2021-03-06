
__author__ = 'AJ'
import json, requests, os, time, timeit, csv, sys
from threading import Thread
import threading
import datetime

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


def log_request(thread, r, func_name):
    '''
    :param r: response
    :return: none
    '''
    with open(thread + '_log_request.txt', 'ab') as f:
        f.write('Function: ' + func_name + '\n')
        f.write('request: ' + str(r.request) + '\n')
        f.write('headers: '+ str(r.headers) + '\n')
        f.write('status code: ' + str(r.status_code) + '\n')
        f.write('histroy: ' + str(r.history) + '\n')
        f.write('Url: ' + str(r.url) + '\n')
        f.write('Reason: ' + str(r.reason) + '\n')
        f.write('_content: ' + str(r._content) + '\n')
        f.write('elapsed: ' + str(r.elapsed) + '\n')
        r = r.json()
        f.write('json: ' + str(r) + '\n')
        f.write('\n\n')
        f.close()


def remove_file(i, sub_dir, json_file_list):
    """
    :param i:
    :param sub_dir:
    :param json_file_list:
    :return:
    """
    os.remove(sub_dir + "/" + json_file_list[i])


def get_token(username, password, key, secret, thread):
    '''
    This Function Retrieves the access token needed to upload data
    '''
    func_name = get_token.__name__
    while True:
        try:
            payload = {'grant_type': "client_credentials", 'username': username, 'password': password, 'scope': 'PRODUCTION'}
            auth = (key, secret)
            r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
            time.sleep(1)
            if r.status_code != 200:
                print thread + " Problem With obtaining Token - Sleep and Continue " + thread + str(datetime.datetime.now())
                time.sleep(30)
                continue
            r = r.json()
            refresh = r["refresh_token"]
            payload = {'grant_type': 'refresh_token', 'refresh_token': refresh}
            r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
            if r.status_code != 200:
                print thread + " Problem With Refreshing Token - Sleep and Continue " + str(datetime.datetime.now())
                time.sleep(30)
                continue
            log_request(thread, r, func_name)
            r = r.json()
            return r['access_token']
        except KeyError:
            continue


def file_list(sub_dir):
    '''
    Obtains the names in the a directory
    :return:File List
    '''
    json_file_list = os.listdir(sub_dir)
    json_files = []
    for elem in json_file_list:
        json_files.append(elem)

    return json_files


def max_file_length(json_file_list):
    num_files = len(json_file_list)
    return num_files


def open_metadata_file(i, sub_dir, json_file_list):
    '''
    This function will change the current file to be uploaded based on the success of experiment_add
    and job_fetch.
    :param i:An interger that
    :return:Metadata json dict
    '''
    jfile = open(os.path.join(sub_dir, json_file_list[i]), "r")
    metadata = jfile.read() #Stores file as json string to close read file.
    jfile.close()
    return metadata


def primary_metadata(metadata):
    '''
    :param metadata: The metadata associated with the experiment. Obtained from the function call open_meta_data
    :return:The Experiment JSON File
    '''
    mfile = json.loads(metadata)
    meta_dict = mfile["metadata"]
    return meta_dict


def additional_metadata(metadata):
    '''
    :param metadata: The metadata json string returned from open_metadata_file
    :return: A dict of additional metadata items
    '''
    metadata = json.loads(metadata)
    add_meta = metadata["additional_metadata"]
    add_dict = {}
    for elem in add_meta:
        add_dict[elem['type']] = elem['text']
    return add_dict


def notebook_add(thread, add_meta, username, token, base_url):
    '''
    :param add_meta:Additional Meta Hash from for giving the proper id and name to note books
    :return: Put response (Dict)
    '''

    class Notebook:
        def __init__(self, nb_name, desc, tp):
            self.metadata = {"name": nb_name, "description": desc, "restricted": False, "type": tp}

    url = base_url + "api/v1/notebooks/?username=%s&token=%s" % (username, token)
    headers = {'Content-type': 'application/json'}
    nb_name = add_meta["Encode Biosample ID"]
    desc = add_meta["Cell Type"]
    tp = "mixed"

    pay = json.dumps(vars(Notebook(nb_name, desc, tp)))
    r = requests.put(url, pay, headers=headers)
    log_request(thread, r, func_name=notebook_add.__name__)
    response_dict = r.json()
    return response_dict


def notebook_search(term, base_url, username, token, thread):
    """
    This function will check if a Notebook already exists A
    :param term:The search term for the notebook (notebook name)
    :return: false if does not exist or dict of notebook vars if does
    """
    url = base_url + "api/v1/notebooks/search/%s/?username=%s&token=%s" % (term, username, token)
    r = requests.get(url)
    log_request(thread, r, func_name=notebook_search.__name__)
    response_dict = r.json()
    try:
        return response_dict["notebooks"][0]
    except IndexError:
        return False


def experiment_add(username, token, metadata, base_url, nb_id, thread):

    '''
    This function will take in a meta data file, iterate through the column in the TSV file and upload experiment
    to CoGe from ENCODE. It will check for current download state, append a list for successful uploads and failure
    list.
    :param username: Username for iPlant Account
    :param token: Token for Requests that is returned from auth_token()
    :param metadata: List of Json Objects )
    :return: None
    '''

    data = metadata
    data = json.loads(data)
    data["notebook_id"] = int(nb_id)
    data = json.dumps(data)

    url = base_url + "api/v1/experiments?username=%s&token=%s" % (username, token)
    headers = {'Content-type': 'application/json'}
    r = requests.put(url, data, headers=headers)
    log_request(thread, r, func_name=experiment_add.__name__)
    response_dict = r.json()
    return response_dict


def write_experiment(wid, thread, exp_name):
    '''

    :param wid:
    :param thread:
    :param exp_ame:
    :return:
    '''
    dat = []
    d1 = [exp_name, wid]
    dat.append(d1)
    with open(thread + '_work_ids.tsv', 'ab') as f:
        log = csv.writer(f, lineterminator="\n", delimiter='\t')
        for elem in dat:
            log.writerow(elem)
        f.close()



def job_fetch(username, wid, base_url, thread, token):
    '''
    :param username: the username for auth
    :param token: The token provided from get_token()
    :param wid: The word id provided by experiment_add()
    :return: A JSON (dict) of the response from experiment_fetch
    '''
    url = base_url + "api/v1/jobs/%d/?username=%s&token=%s" % (wid, username, token)
    r = requests.get(url)
    log_request(thread, r, func_name=job_fetch.__name__)
    response_dict = r.json()
    return response_dict


def check_status(wid, wait, base_url, username, password, key, secret, thread, exp_name):
    '''
    :param username:Your iPlant Username
    :param token: Token from iPlant Auth
    :param wid:Work ID from experiment_add
    :Param wait: Time in seconds until the status is checked again
    :return: The Status of the Job
    '''

    running = True
    while running:
        try:
            token = get_token(username, password, key, secret, thread)
            job = job_fetch(username, wid, base_url, thread, token)
            time.sleep(wait)
            status = job['status']
            time.sleep(wait)
            if status == "Completed":
                print thread + " Work ID: " + str(wid) + " " + status + " " + str(datetime.datetime.now())
                return status
            elif status == "Running":
                continue
            else:
                print thread + " Work ID:" + str(wid) + " " + status + " " + str(datetime.datetime.now())
                return status
        except KeyError:
            print thread + " Error in KeyStatus " + check_status.__name__ + " Continuing " + str(datetime.datetime.now())
            continue


def write_log(exp_name, wid, status, comp_dict, term, thread): # add_meta["File Size"] in the future
    if status == "Completed":
        cdat = []
        comp_dict = json.dumps(comp_dict)
        cl = [exp_name, wid, status, comp_dict]
        cdat.append(cl)
        term = term.replace(":","_")

        with open("logs/" + "Completed_Log_" + term + "_" + thread + ".tsv" , "ab") as f:
            comp_log = csv.writer(f, lineterminator="\n", delimiter='\t')
            for elem in cdat:
                comp_log.writerow(elem)
            f.close()

    else:
        fdat = []
        comp_dict = json.dumps(comp_dict)
        fl = [exp_name, wid, status, comp_dict]
        fdat.append(fl)
        term = term.replace(":","_")
        with open("logs/" + "Failed_Log_" + term + "_" + thread + ".tsv", "ab") as f:
            comp_log = csv.writer(f, lineterminator="\n", delimiter='\t')
            for elem in fdat:
                comp_log.writerow(elem)
            f.close()


def split_jobs(file_list, size):
    """
    :param file_list: The return of max_files file_list function. Specifies how many tasks need to be performed
    :param size: The number of task to be performed
    :return: A list of ranges that speficy the number of tasks
    """

    ranges = []
    splitsize = 1.0/size*len(file_list)
    for i in range(size):
            ranges.append(file_list[int(round(i*splitsize)):int(round((i+1)*splitsize))])
    return ranges


def file_remove(sub_dir, i, json_file_list):
    """
    This function removes the json file if the job is completed
    :param sub_dir: The sub directory where the json file is located
    :param i: The current index of the file
    :param json_file_list: The list of files associated with the index
    :return:None
    """
    os.remove(sub_dir + "/" + json_file_list[i])


def run_all(min, max, client):
    thread = threading.current_thread().name
    start = time.time()
    # Obtain user information
    user = user_data(client)
    username = user["username"]
    password = user["password"]
    secret = user["secret"]
    key = user["key"]

    # Set directories and obtain metadata
    base_url = "https://geco.iplantcollaborative.org/coge/"
    json_file_list = file_list(sub_dir)

    wait = 120


    for i in range(min, max + 1):
        token = get_token(username, password, key, secret, thread)
        print thread + " Obtaining New token " + token + " " + str(datetime.datetime.now())
        metadata = open_metadata_file(i, sub_dir, json_file_list)
        pri_meta = primary_metadata(metadata)
        exp_name = pri_meta["name"]
        add_meta = additional_metadata(metadata)
        term = add_meta["Encode Biosample ID"]

        nb_check = notebook_search(term, base_url, username, token, thread)


        if nb_check == False:
             nb_id = notebook_add(thread, add_meta, username, token, base_url)["id"]
             print thread + " Notebook ID: " + str(nb_id) + " " + str(datetime.datetime.now())
        else:
            nb_id = notebook_search(term, base_url, username, token, thread)["id"]
            print thread + " Notebook ID: " + str(nb_id) + " " + str(datetime.datetime.now())

        wid = experiment_add(username, token, metadata, base_url, nb_id, thread)['id']
        write_experiment(wid,thread,exp_name)
        print thread + " Work ID: " + str(wid) + " submitted - " + str(datetime.datetime.now())
        print thread + " Removing " + json_file_list[i] + " from files - " + str(datetime.datetime.now())
        file_remove(sub_dir, i, json_file_list)
        status = check_status(wid, wait, base_url, username, password, key, secret, thread, exp_name)
        comp_dict = json.dumps(job_fetch(username, wid, base_url, thread, token))
        write_log(exp_name, wid, status, comp_dict, term, thread)

if __name__ == '__main__':
    go = sys.argv[1]
    sub_dir = '/home/ajstangl/encode/jsons'
    json_files = file_list(sub_dir)
    total_files = max_file_length(json_files)
    temp = split_jobs(range(total_files), 4)
    w1 = temp[0]
    w2 = temp[1]
    w3 = temp[2]
    w4 = temp[3]


    client1 = 'client1.json'
    client2 = 'client2.json'
    client3 = 'client3.json'
    client4 = 'client4.json'

    p1 = Thread(target=run_all, args=(min(w1), max(w1), client1))
    p2 = Thread(target=run_all, args=(min(w2), max(w2), client2))
    p3 = Thread(target=run_all, args=(min(w3), max(w3), client3))
    p4 = Thread(target=run_all, args=(min(w4), max(w4), client4))
    # entry = int(raw_input("Select Which Thread to Process 1 - 4: "))
    # while entry != 1 or entry != 2 or entry != 3  or entry != 4:
    #     if entry == 1:
    #         print "Starting Thread 1 "
    #         p1.start()
    #         break
    #     elif entry == 2:
    #         print "Starting Thread 2 "
    #         p2.start()
    #         break
    #     elif entry == 3:
    #         print "Starting Thread 3 "
    #         p3.start()
    #         break
    #     elif entry == 4:
    #         print "Starting Thread 4 "
    #         p4.start()
    #         break
    #     else:
    #         print "Invalid Entry"
    #         entry = int(raw_input("Select Which Thread to Process 1 - 4: "))
    #
    if go == str(1):
        p1.start()
    elif go == str(2):
        p2.start()
    elif go == str(3):
        p3.start()
    elif go == str(4):
        p4.start()
    else:
        p1.start()
        p2.start()
        p3.start()
        p4.start()