__author__ = 'AJ'
import urllib
import csv

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


