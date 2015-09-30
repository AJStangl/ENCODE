__author__ = 'AJ'
import json, requests, os, time, csv


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


def experiment_detail(metadata):
    '''
    :param metadata: The metadata associated with the experiment. Obtained from the function call open_meta_data
    :return:The Experiment JSON File
    '''
    mfile = json.loads(metadata)
    mfile_dict = mfile["metadata"]
    return mfile_dict


def notebook_add(username, token, base_url, metadata):
    '''

    :param username: Iplant User ID
    :param token: Token From Agave API
    :param base_url: Base URL for API
    :return: Notebook ID
    '''
    class Notebook:

        def __init__(self, nb_name, desc, tp):
            self.metadata = {"name": nb_name, "description": desc, "restricted": False, "type": tp}

    url = base_url + "api/v1/notebooks/?username=%s&token=%s" % (username, token)
    mdata = json.loads(metadata)
    adata = mdata["additional_metadata"]

    for elem in adata:
        if elem["text"] == "Bio_Sample":
            temp = elem["type"]
    nb_name = temp

    desc = mdata["metadata"]["description"]
    tp = "mixed"
    pay = json.dumps(vars(Notebook(nb_name, desc, tp)))
    r = requests.put(url,pay)
    resp_dict = r.json()
    return resp_dict


def experiment_add(username, token, metadata, base_url):

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


def check_status(username, token, wid, wait):
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
            running = False
            return status
        elif status == "Running":
            continue
        else:
            running = False
            return status


def write_log(exp_name, wid, status, comp_dict):
    if status == "Completed":
        with open("Completed_Log.txt", "a") as comp_log:
            comp_log.write(exp_name + "\n" + str(wid) + "\n" + status + "\n")
            comp_log.write(comp_dict)
            comp_log.write("\n" + "#####" + "\n")
            comp_log.close()
    else:
        with open("Failed_Log.txt", "a") as comp_log:
            comp_log.write(exp_name + "\n" + str(wid)+ "\n" + status + "\n")
            comp_log.write(comp_dict)
            comp_log.write("\n" + "#####" + "\n")
            comp_log.close()
    return


def next_job(i, status):
    '''

    :param status: The status of
    :return: i
    '''
    if status == "Completed":
        i += 1
    elif status == "Failed":
        i += 1
    return i




# Sudo Main
login = user_data("login.json")
username = login["username"]
base_url = "https://geco.iplantcollaborative.org/coge/"
# sub_dir = "C:\Users\AJ\PycharmProjects\Encode\jsons"
sub_dir="/home/ajstangl/encode/jsons" # for geco

json_file_list = file_list(sub_dir)
max_files = len(json_file_list)
wait = 60
i = 0
run_once = 0 # Need a better logic gate for new note book - unless performed biosample by biosample.
while i < max_files:
    token = get_token(username, password=login["password"], key=login["key"], secret=login["secret"])
    metadata = open_metadata_file(i, sub_dir, json_file_list)
    if run_once == 0:
        nb_id = notebook_add(username, token, base_url, metadata)["id"]
        run_once = 1
    print nb_id
    metadata = json.loads(metadata)
    metadata["notebook_id"] = nb_id
    metadata = json.dumps(metadata)
    exp_name = experiment_detail(metadata)["name"]
    print exp_name
    wid = experiment_add(username, token, metadata, base_url)['id']
    print wid
    status = check_status(username, token, wid, wait)
    print status
    comp_dict = json.dumps(job_fetch(username, token, wid, base_url))
    write_log(exp_name, wid, status, comp_dict)
    i = next_job(i, status)






































