__author__ = 'AJ'
def tv_to_json(metadata):
    import csv
    """
    This function will convert the metadata file to a json object for upload to CoGe

    :param metadata: A metadata.txt in TSV form
    :return: A json object of the metadata file

    Here is a sample JSON request body for experiment_add.json:
{
   "restricted": true,
   "genome_id": 16911,
   "version": "1",
   "name": "DiffExpr1",
   "description": "Expression measurements from tissue X with treatment Y.",
   "source_name": "JGI",
   "items": [
      { "type": "irods", "path": "/iplant/home/coge/coge_data/arabidopsis/experimental_condition1.csv" }
   ]
}
    """
jsfile = file()
