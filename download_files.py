__author__ = 'AJ'
'''
This function will access all files in the the enncode database, retreive the download
url's in the the metadata file and download the files to the local directory.
'''

import urllib,csv

with open("bam_metadata_encode.tsv", 'r') as infile:
    infile = csv.reader(infile, delimiter='\t')

    url = []

    for row in infile:
        if row[12] != "Download_Link":
            url.append(row[12])

    for elem in url:
        fname = elem.split("/")
        fname = fname[-1]
        urllib.urlretrieve(elem, fname)


