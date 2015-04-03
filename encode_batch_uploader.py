__author__ = 'AJ'

def coge_upload(username, password):
    """
    Incomplete  code that will be used to upload bam files from encode directly to coge batchupload/loadexperiment

    :param username: The username for your iplant account
    :param password: The password for your iplant account
    :return: None
    """
    import requests, json, urllib2

    base_url = "https://genomevolution.org/coge/api/v1/"
    auth_url = "https://foundation.iplantcollaborative.org/auth-v1/"
    gid = "25577" # HG19 Genome ID

    '''
    Requests the Authentication Token for Data Upload
    '''
    r = requests.post(auth_url, auth=(username, password))
    auth_dict = r.json()
    token = auth_dict["result"]["token"]
    username = "ajstangl"


    search = requests.get(base_url"/organisms/search/gid+?username=%s&token=%s") % (username, token)
    rep = search.json()
    return









