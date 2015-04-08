__author__ = 'AJ'

def auth_token(username, password):
    """
    Incomplete  code that will be used to upload bam files from encode directly to coge loadexperiment

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




    return token

token = auth_token("ajstangl", "Bio Informatics1")
metadata = "bam_metadata_encode.txt"

def experiment_add(username, token, metadata):
    '''
    This function will take in a meta data file, iterate through the column in the TSV file and upload experiment
    to CoGe from ENCODE. It will check for current download state, append a list for successful uploads and failure
    list.

    :param username: Username for iPlant Account
    :param token: Token for Requests that is returned from auth_token()
    :param metadata: Metadata file in tsv form (named bam_metadata_encode.txt)
    :return: None
    '''
    import requests, json, urllib2, csv
    gid = "25577" # HG19 Genome ID

    download_url = []
    base_url = "https://genomevolution.org/coge/api/v1/experiments?username=%s&token=%s" % (username, token)
    r = requests.get(base_url)
    print r.status_code

    # token = open(metadata, "r")
    # metadata = csv.reader(metadata, delimiter="\t")
    # for row in metadata:
    #     print row





experiment_add("ajstangl",token, metadata)










