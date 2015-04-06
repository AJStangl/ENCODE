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
        # Places URL for Download into URL list without adding the header
        for row in infile:
            if row[12] != "Download_Link":
                url.append(row[12])

        # Splits the elem in the URL list and retrieves the last elem corresponding to the file name
        # Requies a filename(fname) and download url(elem)
        for elem in url:
            fname = elem.split("/")
            fname = fname[-1]
            urllib.urlretrieve(elem, fname)

    return

download_bam("bam_metadata_encode.txt")