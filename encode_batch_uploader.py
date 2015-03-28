__author__ = 'AJ'
import requests,json,base64


base_url = "https://genomevolution.org/coge/api/v1/"
auth_url = "https://iplantcollaborative.org/auth-v1/renew/"
gid = "25577"

## Authenticate
headers = {'content-type': 'application/json'}
payload = {"username": "ajstangl","password": base64.b64encode("Bio Informatics1")}
response = requests.post(auth_url,data=json.dumps(payload),headers=headers)


print response

##contents = requests.get(base_url + "/genomes/search/" + gid)
##
##response = contents.json()
##
##print response


##payload = json.dumps({"name": "Dog_Shit","description": "Dog Fecal Matter Assay"})
##headers = {'content-type': 'application/json'}
##response = requests.post(base_url + "organisms",data=json.dumps(payload),headers=headers)
##print response



