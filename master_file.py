__author__ = 'AJ'
from better_extractor import  get_exp_url, metadata_extractor
get_exp_url()
exp_url = get_exp_url()
test = exp_url[0:1]
metadata_extractor(test)
