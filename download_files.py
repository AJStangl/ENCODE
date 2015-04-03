__author__ = 'AJ'
def download_bam(metadata):
    '''
    This function will access all files in the the enncode database, retrieve the download
    url's in the the metadata file and download the files to the local directory.

    Input: A meta data file in TSV form that is written by bam_metadata_encode Script

    Output: None

    Return: None
    '''

    import urllib,csv

    with open(metadata, 'r') as infile:
        infile = csv.reader(infile, delimiter='\t')

        url = []

        for row in infile:
            if row[12] != "Download_Link":
                url.append(row[12])

        for elem in url:
            fname = elem.split("/")
            fname = fname[-1]
            urllib.urlretrieve(elem, fname)
    return

