__author__ = 'AJ'
import requests, json, urllib2

base_url = "https://genomevolution.org/coge/api/v1/"
auth_url = "https://foundation.iplantcollaborative.org/auth-v1/"
gid = "25577" # HG19 Genome ID

'''
Requests the Authentication Token for Data Upload
'''
r = requests.post(auth_url, auth=("ajstangl", "Bio Informatics1"))
auth_dict = r.json()
token = auth_dict["result"]["token"]
username = "ajstangl"


search = requests.get(base_url"/organisms/search/gid+?username=%s&token=%s") % (username, token)
rep = search.json()
print rep










