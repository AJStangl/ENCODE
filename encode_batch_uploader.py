__author__ = 'AJ'
import json, requests, os, time, timeit, csv
from datetime import datetime
from collections import deque


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


def log_request(r, func_name):
    '''

    :param r: response
    :return: none
    '''
    with open('_log_requst.txt', 'ab') as f:
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
        f.write(datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
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


def get_token(username, password, key, secret):
    '''
    This Function Retrieves the access token needed to upload data
    '''
    func_name = get_token.__name__
    while True:
        payload = {'grant_type': "client_credentials", 'username': username, 'password': password, 'scope': 'PRODUCTION'}
        auth = (key, secret)
        r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
        if r.status_code != 200:
            print " Problem With obtaining Token - Sleep and Continue "
            continue
        r = r.json()
        refresh = r["refresh_token"]
        payload = {'grant_type': 'refresh_token', 'refresh_token': refresh}
        r = requests.post('https://agave.iplantc.org/token', data=payload, auth=auth)
        if r.status_code != 200:
            print "Problem With Refreshing Token - Sleep and Continue"
            time.sleep(30)
            continue
        log_request(r, func_name)
        r = r.json()
        print "Obtained Token " + r['access_token']
        return r['access_token']


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


def notebook_search(term, add_meta, base_url, username, token):
    """
    This function will check if a Notebook already exists A
    :param term:The search term for the notebook (notebook name)
    :return: false if does not exist or dict of notebook vars if does
    """
    while True:
        url = base_url + "api/v1/notebooks/search/%s/?username=%s&token=%s" % (term, username, token)
        r = requests.get(url)
        if r.status_code == 200:
            log_request(r, func_name=notebook_search.__name__)
            response_dict = r.json()
            try:
                return response_dict["notebooks"][0]['id']
            except IndexError:
                #time.sleep(10)
                print " notebook not found for " + term + " adding new notebook "
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
                if r.status_code == 200:
                    log_request(r, func_name="Notebook add")
                    response_dict = r.json()
                    return response_dict['id']

                else:
                    print ' Error in notebook search '  + str(r.content)
                    log_request(r, func_name= notebook_search.__name__)
                    continue


def experiment_add(username, token, metadata, base_url, nb_id, password, key, secret):

    '''
    This function will take in a meta data file, iterate through the column in the TSV file and upload experiment
    to CoGe from ENCODE. It will check for current download state, append a list for successful uploads and failure
    list.

    :param username: Username for iPlant Account
    :param token: Token for Requests that is returned from auth_token()
    :param metadata: List of Json Objects )
    :return: None
    '''
    while True:
        data = metadata
        data = json.loads(data)
        data["notebook_id"] = int(nb_id)
        data = json.dumps(data)
        url = base_url + "api/v1/experiments?username=%s&token=%s" % (username, token)
        headers = {'Content-type': 'application/json'}
        r = requests.put(url, data, headers=headers)
        if r.status_code == 200:
            log_request(r, func_name=experiment_add.__name__)
            response_dict = r.json()
            return response_dict
        else:
            log_request(r, func_name=experiment_add.__name__)
            token = get_token(username, password, key, secret)
            print " Error in Adding Experiment: " + str(r._content)
            continue


def job_fetch(username, wid, base_url, token, wait):
    '''
    :param username: the username for auth
    :param token: The token provided from get_token()
    :param wid: The word id provided by experiment_add()
    :return: A JSON (dict) of the response from experiment_fetch
    '''
    #while True:
    url = base_url + "api/v1/jobs/%d/?username=%s&token=%s" % (wid, username, token)
    r = requests.get(url)
    log_request(r, func_name=job_fetch.__name__)
    #if r.status_code == 200:
    response_dict = r.json()
    #if response_dict['status'] == "Running":
        #time.sleep(wait)
        #continue
    #else:
    return response_dict


def write_log(exp_name, wid, status, comp_dict, system_elapsed, term, add_meta):
    if status == "Completed":
        cdat = []
        fsize = add_meta["File Size"]
        elapsed = []
        for elem in comp_dict['tasks']:
            if elem['elapsed'] != None:
                elapsed.append(elem['elapsed'])
        elapsed = sum(elapsed)
        cl = [exp_name, wid, status, comp_dict, fsize, elapsed, system_elapsed]
        cdat.append(cl)
        with open("logs/" + "Completed_Log_" + term + "_" +  ".tsv" , "ab") as f:
            comp_log = csv.writer(f, lineterminator="\n", delimiter='\t')
            for elem in cdat:
                comp_log.writerow(elem)
            f.close()

    else:
        fdat = []
        elapsed = []
        fsize = add_meta["File Size"]
        for elem in comp_dict['tasks']:
            if elem['elapsed'] != None:
                elapsed.append(elem['elapsed'])
        elapsed = sum(elapsed)
        fl = [exp_name, wid, status, comp_dict, fsize, elapsed, system_elapsed]
        fdat.append(fl)
        with open("logs/" + "Failed_Log_" + term + "_" + ".tsv", "ab") as f:
            comp_log = csv.writer(f, lineterminator="\n", delimiter='\t')
            for elem in fdat:
                comp_log.writerow(elem)
            f.close()


def next_job(i, status):
    """
    :param status: The status of
    :return: i
    """
    if status == "Completed":
        i += 1

    elif status == "Failed":
        i += 1
    return i


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


def run_job(json_file_list, i):

    start_time = timeit.default_timer()

    # Obtain user information
    user = user_data('login.json')
    username = user["username"]
    password = user["password"]
    secret = user["secret"]
    key = user["key"]
    # Set directories and obtain metadata
    base_url = "https://geco.iplantcollaborative.org/coge/"
    # sub_dir = '/home/ajstangl/encode/jsons'
    token = get_token(username, password, key, secret)
    metadata = open_metadata_file(i, sub_dir, json_file_list)
    pri_meta = primary_metadata(metadata)
    add_meta = additional_metadata(metadata)
    term = add_meta["Encode Biosample ID"]
    nb_id = notebook_search(term, add_meta, base_url, username, token)
    print "Notebook ID " + str(nb_id)
    exp_name = pri_meta["name"]
    print "Experiment Name - " + exp_name
    wid = experiment_add(username, token, metadata, base_url, nb_id, password, key, secret)['id']
    print "Work ID: " + str(wid) + " submitted"
    file_remove(sub_dir,json_file_list,i)
    return {"wid":wid, "exp_name":exp_name}

'''
        else:
            print wid_lst
            for elem in wid_lst:
                comp_dict = job_fetch(username, wid, base_url, token, wait)
                print str(elem) + ' is running'
                status = comp_dict['status']
                time.sleep(10)
                if status == "Running":
                    continue
                else:
                    system_elapsed = timeit.default_timer() - start_time
                    write_log(exp_name,wid,status, comp_dict, system_elapsed, term, add_meta)
                    wid_lst.remove(elem)
                    i = i + 1
                    pass

        else:
            continue
            # comp_dict = job_fetch(username, wid, base_url, token, wait)
            # print str(elem) + ' is running'
            # status = comp_dict['status']
            # time.sleep(10)
            if status == "Running":
                continue
            else:
                system_elapsed = timeit.default_timer() - start_time
                write_log(exp_name,wid,status, comp_dict, system_elapsed, term, add_meta)
                wid_lst.remove(elem)
                i = i + 1
                pass


                comp_dict = job_fetch(username, wid, base_url, token, wait)
                status = comp_dict['status']
                print str(wid) + " " + status

                if status == "Completed":
                    system_elapsed = timeit.default_timer() - start_time
                    write_log(exp_name, wid, status, comp_dict, system_elapsed, term, add_meta)
                    queue.remove(queue[j])
                    i = i + 1
                    queue.insert(j,json_file_list[i])
                    print "Moving to Next Job"
                    continue

                elif status == "Failed":
                    system_elapsed = timeit.default_timer() - start_time
                    write_log(exp_name, wid, status, comp_dict, system_elapsed, term,add_meta)
                    queue.remove(queue[j])
                    i = i + 1
                    queue.insert(j,json_file_list[i])
                    print "Moving to Next Job"
                    continue



        except IndexError:
            token = get_token(username, password, key, secret)
            for j in range(len(queue)):
                metadata = open_metadata_file(j, sub_dir, json_file_list)
                pri_meta = primary_metadata(metadata)
                add_meta = additional_metadata(metadata)
                term = add_meta["Encode Biosample ID"]
                nb_id = notebook_search(term, add_meta, base_url, username, token)
                print "Notebook ID " + str(nb_id)
                exp_name = pri_meta["name"]
                wid = experiment_add(username, token, metadata, base_url, nb_id, password, key, secret)['id']
                print "Work ID: " + str(wid) + " submitted"
                print j
                if j != len(queue):
                    continue
                else:
                    comp_dict = job_fetch(username, wid, base_url, token, wait)
                    status = comp_dict['status']
                    print str(wid) + " " + status
                    if status == "Completed" and len(queue) == 4:
                        system_elapsed = timeit.default_timer() - start_time
                        write_log(exp_name, wid, status, comp_dict, system_elapsed, term, add_meta)



                    elif status == "Failed":
                        system_elapsed = timeit.default_timer() - start_time
                        write_log(exp_name, wid, status, comp_dict, system_elapsed, term,add_meta)
                        print "Moving to Next Job"

      for i in range(min, max + 1):
        token = get_token(username, password, key, secret)
        metadata = open_metadata_file(i, sub_dir, json_file_list)

        pri_meta = primary_metadata(metadata)
        add_meta = additional_metadata(metadata)
        term = add_meta["Encode Biosample ID"]

        nb_id = notebook_search(term, add_meta, base_url, username, token, password, key, secret)

        print "Notebook ID " + str(nb_id)

        exp_name = pri_meta["name"]

        print" Experiment Name: " + exp_name

        wid = experiment_add(username, token, metadata, base_url, nb_id, password, key, secret)['id']

        print "Work ID: " + str(wid) + " submitted"

        comp_dict = job_fetch(username, wid, base_url, password, key, secret, token, wait)

        status = comp_dict['status']

        print str(wid) + " " + status

        if status == "Completed":
            system_elapsed = timeit.default_timer() - start_time
            write_log(exp_name, wid, status, comp_dict, system_elapsed, term, add_meta)
        elif status == "Failed":
            system_elapsed = timeit.default_timer() - start_time
            write_log(exp_name, wid, status, comp_dict, system_elapsed, term,add_meta)

        print " Moving to Next Job "
        '''






if __name__ == '__main__':
    i = 0
    upload_list = []
    sub_dir = 'C:\Users\AJ\PycharmProjects\Encode\jsons'
    json_file_list = file_list(sub_dir)
    run_job(json_file_list)




