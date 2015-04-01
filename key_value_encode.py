import requests

HEADERS = {'accept': 'application/json'}
URL = "https://www.encodeproject.org/experiments/ENCSR000CVM"
response = requests.get(URL, headers=HEADERS)

exp_dict = response.json()
# with open ('key_dict.txt', 'w') as test:
"""For Keys in general dict object"""


"""Test for keys and values in files sub key"""
i = 0
limit = len(exp_dict["files"])
while i < limit:
    if exp_dict["files"][i]["file_format"] == "bam":
        for k , v in exp_dict["files"][i]["replicate"]["experiment"].iteritems():
             print k
             print v
             print "\n"
        print "######"

    
        

    i = i + 1


