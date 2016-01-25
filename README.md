# ENCODE
Major project for the CoGe Lab 
* https://genomevolution.org/CoGe/
* http://www.lyonslab.net/

This pipeline automates the data extraction from https://www.encodeproject.org/ and uploads BAM or FASTQ files to the CoGe development server 
for genome visualization, comparison, and later projects where functional genomic data from human may be of interest. 

There are two primary programs for the ENCODE project : 
* <p><b>metadata_extractor
* uploader.py</b>.</p>

<p><b>Usage of ENCODE</p></b>
<p>Python Modules:</p>
* requests 
* json
* os
* sys
* csv 
* threading 
* datetime
* time 
<p>All functions use raw input from user for ease of use and not dependent on obscure system arguments</p>
<p><b>metadata_extractor.py</p></b>
* Functions 
 - get_exp_url(search)
    <p>Input: Endpoint URL for Assays in encode </p>
    <p>Ex) ?type=Experiment&assay_term_name=ChIP-seq&assembly=hg19</p>
      <p>- All ChIP-seq experiments for Hg19 Human Genome </p>
   <p> Output: List of experiment URLS</p>
  -  metadata_extractor(exp_url_list, filename, filetype)
    <p>Input: Experiment URLS from get_exp_url, filename, and filetype</p> 
    <p>Output: TSV of many different types of metadata and URLs where data can be retrived by CoGe API </p>
  - add_data(self, in_file, genome_id)
    <p>Input: The name of the TSV file generated by metadata extractor </p>
    <p>Output: Directory named JSON located in the current working directory where the script it deployed and a series of JSON files each
    representing a single experiment to be uploaded. 
    
  <p><b>uploader.py</p></b>
  - Consists of various functions that will: 
    <p>1) Authenticate User Credentials with Agave API </p>
    <p>2) Log all network communications with CoGe API </p>
    <p>3) Extract Primary and Secondary Metadata from JSON and format as a JSON string to communicate to CoGe API </p>
    <p>4) Add Experiment notebook for each Cell Line</p>
    <p>5) Add experiment to appropriate genome and notebook </p>
    <p>6) Report if the experiment failed or succeeded in data loading</p>
    <p>7) Multithreaded Capability to decrease load time by removing serialized method of data upload. </p>
  
 <p>Example Usage: </p>
 <p>python uploader.py 5</p>
 <p>Speficying 1 - 4 will inform the program to use N number of threads for parallel data transfer. 5 Indicates run all</p>
  
