__author__ = 'AJ'
import json, requests, os, time, csv, timeit
from threading import Thread
import threading


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
    content_dict = json.loads(r.content)
    token = content_dict["access_token"]
    return token


def file_list(sub_dir):
    '''
    Obtains the names in the a directory
    :return:File List
    '''
    json_file_list = os.listdir(sub_dir)
    return json_file_list


def max_file_length(sub_dir,json_file_list):
    max_file_lenght = len(json_file_list(sub_dir))


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


def notebook_add(add_meta, username,token, base_url):
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
    resp_dict = r.json()
    return resp_dict


def notebook_search(term, base_url, username, token):
    """
    This function will check if a Notebook already exists A
    :param term:The search term for the notebook (notebook name)
    :return: false if does not exist or dict of notebook vars if does
    """
    url = base_url + "api/v1/notebooks/search/%s/?username=%s&token=%s" % (term, username, token)
    r = requests.get(url)
    resp_dict = r.json()
    try:
        return resp_dict["notebooks"][0]
    except IndexError:
        return False


def experiment_add(username, token, metadata, base_url, nb_id):

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
    rep_dict = r.json()
    return rep_dict


def job_fetch(username, token, wid, base_url):
    '''
    :param username: the username for auth
    :param token: The token provided from get_token()
    :param wid: The word id provided by experiment_add()
    :return: A JSON (dict) of the response from experiment_fetch
    '''
    url = base_url + "api/v1/jobs/%d/?username=%s&token=%s" % (wid, username, token)
    r = requests.get(url)
    comp_dict = r.json()
    return comp_dict


def check_status(username, token, wid, wait, base_url):
    '''

    :param username:Your iPlant Username
    :param token: Token from iPlant Auth
    :param wid:Work ID from experiment_add
    :Param wait: Time in seconds until the status is checked again
    :return: The Status of the Job
    '''

    running = True
    while running:
        status = job_fetch(username, token, wid, base_url)["status"]
        time.sleep(wait)
        if status == "Completed":
            return status
        elif status == "Running":
            continue
        else:
            return status


def write_log(exp_name, wid, status, comp_dict, elapsed):
    if status == "Completed":
        with open("Completed_Log.txt", "a") as comp_log:
            comp_log.write(exp_name + "\n" + str(wid) + "\n" + status + "\n")
            comp_log.write(comp_dict)
            comp_log.write("\n" + "Time elapsed: " + str(elapsed) + "\n")
            comp_log.write("\n" + "#####" + "\n")
            comp_log.close()
    else:
        with open("Failed_Log.txt", "a") as comp_log:
            comp_log.write(exp_name + "\n" + str(wid) + "\n" + status + "\n")
            comp_log.write(comp_dict)
            comp_log.write("\n" + "Time elapsed: " + str(elapsed) + "\n")
            comp_log.write("\n" + "#####" + "\n")
            comp_log.close()
    return


def next_job(start, status):
    '''

    :param status: The status of
    :return: i
    '''
    if status == "Completed":
        start += 1
    elif status == "Failed":
        start += 1
    return start


def split_jobs(file_list, size):
    """
    :param jobs: The return of max_files file_list function. Specifies how many tasks need to be performed
    :param size: The number of task to be performed
    :return: A list of ranges that speficy the number of tasks
    """

    ranges = []
    splitsize = 1.0/size*len(file_list)
    for i in range(size):
            ranges.append(file_list[int(round(i*splitsize)):int(round((i+1)*splitsize))])
    return ranges


def run_all(min, max):
    lock = threading.Lock()
    start_time = timeit.default_timer()
    login = user_data("login.json")
    username = login["username"]
    base_url = "https://geco.iplantcollaborative.org/coge/"
    json_file_list = file_list(sub_dir)
    wait = 5

    for i in range(min, max+1):
        token = get_token(username, password=login["password"], key=login["key"], secret=login["secret"])
        metadata = open_metadata_file(i, sub_dir, json_file_list)
        pri_meta = primary_metadata(metadata)
        add_meta = additional_metadata(metadata)
        term = add_meta["Encode Biosample ID"]
        nb_check = notebook_search(term, base_url, username, token)
        if nb_check == False:
            nb_id = notebook_add(add_meta, username, token, base_url)["id"]
            print "Notebook ID: " + str(nb_id)
        else:
            nb_id = notebook_search(term, base_url, username, token)["id"]
        exp_name = pri_meta["name"]
        print "Eexperiment Name: "+ exp_name
        wid = experiment_add(username, token, metadata, base_url, nb_id)['id']
        print "Work ID " + str(wid)
        status = check_status(username, token, wid, wait, base_url)
        comp_dict = json.dumps(job_fetch(username, token, wid, base_url))

        if status == "Complete":
            elapsed = timeit.default_timer() - start_time
            lock.acquire()
            write_log(exp_name, wid, status, comp_dict, elapsed)
            lock.release()
        print exp_name + ":" + str(wid) + " " + "complete"



if __name__=='__main__':
    # sub_dir = "C:\Users\AJ\PycharmProjects\Encode\jsons"
    # sub_dir="/home/ajstangl/encode/jsons" # for geco
    sub_dir = "C:\Users\AJ\PycharmProjects\Encode\Test J"
    total_files = len(file_list(sub_dir))
    temp = split_jobs(range(total_files), 4)
    w1 = temp[0]
    w2 = temp[1]
    w3 = temp[2]
    w4 = temp[3]

    p1 = Thread(target=run_all, args=(min(w1), max(w1)))
    p2 = Thread(target=run_all, args=(min(w2), max(w2)))
    p3 = Thread(target=run_all, args=(min(w3), max(w3)))
    p4 = Thread(target=run_all, args=(min(w4), max(w4)))

    p1.start()
    time.sleep(10)
    p2.start()
    time.sleep(10)
    p3.start()
    time.sleep(10)
    p4.start()

















































