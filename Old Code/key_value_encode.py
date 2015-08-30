import requests

HEADERS = {'accept': 'application/json'}
URL = "https://www.encodeproject.org/experiments/ENCSR000ASW/"
response = requests.get(URL, headers=HEADERS)

exp_dict = response.json()
# with open ('key_dict.txt', 'w') as test:
"""For Keys in general dict object"""


"""Test for keys and values in files sub key"""
i = 0
limit = len(exp_dict["files"])


with open('bam_metadata_encode.txt', 'w') as metadata:
        metadata.write(
            "Name\tExperiment_Name\tDescription\tAssay\tReplicate\tCell_Type\tBio_Sample\tTarget\tAssembly\tLab\tDate"
            "\tVersion\tSource\tDownload_Link\tSource_Link\tSequencer\tRun_Type\tFile_Type\tBiosample_term_id"
            "\tFile_Size\n")
        while i < limit:
            if exp_dict["files"][i]["file_format"] == "bam":
                data_dict = {}

                data_dict.fromkeys(
                    ["Filename", "Name", "Description", "Assay", "Replicate", "Cell_type", "Bio_Sample", "Target",
                     "Assembly", "Lab", "Date", "Version", "Source", "Download_Link", "Source_Link", "Sequencer",
                     "Run_Type", "File_Type", "Biosample_term_id", "File_Size"])

                data_dict["Filename"] = exp_dict["files"][i]["href"]
                filename = data_dict["Filename"]
                temp = filename.split("/")
                data_dict["Filename"] = exp_dict["files"][i]["href"]
                filename = data_dict["Filename"]
                temp = filename.split("/")
                metadata.write(temp[4] + "\t")


                # Name
                metadata.write(exp_dict["accession"] + "\t")

                # Description
                try:
                    if exp_dict["files"][i]["replicate"]["experiment"]["description"] != "":
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["description"].replace("\n","").replace("\r","") + "\t")
                    else:
                        metadata.write("Not Listed" + "\t")
                except KeyError:
                    if exp_dict["description"] != "":
                        metadata.write(exp_dict["description"] + "\t")
                    else:
                        metadata.write("Not Listed" + "\t")

                # Assay
                try:
                    if exp_dict["files"][i]["replicate"]["experiment"]["assay_term_name"] != "":
                        metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["assay_term_name"] + "\t")
                    else:
                        metadata.write("Not Listed" + "\t")
                except KeyError:
                    if exp_dict["assay_term_name"] != "":
                        metadata.write(exp_dict["assay_term_name"] + "\t")
                    else:
                        metadata.write("Not Listed" + "\t")

                # Replicate
                try:
                    metadata.write(str(exp_dict["files"][i]["replicate"]["biological_replicate_number"]) + "\t")

                except KeyError:
                    metadata.write("Not Listed" + "\t")

                # Cell_Type
                try:
                    metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["biosample_term_name"] + "\t")
                except KeyError:
                    metadata.write(exp_dict["biosample_term_name"] + "\t")

                # Bio_Sample
                try:
                    metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["biosample_type"] + "\t")
                except KeyError:
                    metadata.write(exp_dict["biosample_type"] + "\t")

                # Target
                try:
                    metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["target"]["label"] + "\t")
                except KeyError:
                    metadata.write("Not Listed" + "\t")

                # Assembly
                try:
                    metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["assembly"][0] + "\t")
                except (KeyError, IndexError):
                    metadata.write(exp_dict["files"][i]["assembly"] + "\t")

                # Lab
                try:
                    metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["lab"]["title"] + "\t")
                except KeyError:
                    metadata.write(exp_dict["files"][i]["lab"]["title"] + "\t")

                # Date
                try:
                    metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["date_released"] + "\t")
                except KeyError:
                    metadata.write(exp_dict["files"][i]["date_created"] + "\t")

                # Version
                Version = data_dict["Version"] = "1"
                metadata.write(Version + "\t")

                # Source
                metadata.write(exp_dict["award"]["project"] + "\t")

                # Download_Link
                metadata.write("https://www.encodeproject.org" + exp_dict["files"][i]["href"] + "\t")

                # Source_Link
                metadata.write(URL + "\t")

                # Sequencer
                try:
                    metadata.write("Not Listed" + "\t")
                except KeyError:
                    metadata.write(exp_dict["files"][i]["platform"]["title"] + "\t")

                # Run_Type
                try:
                    metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["run_type"] + "\t")
                except KeyError:
                    metadata.write("not listed" + "\t")

                # File_Type
                metadata.write(exp_dict["files"][i]["file_format"] + "\t")

                # Biosample_Term_ID
                try:
                    metadata.write(exp_dict["files"][i]["replicate"]["experiment"]["biosample_term_id"] + "\t")
                except KeyError:
                    metadata.write(exp_dict["biosample_term_id"] + "\t")


                # File_Size
                fsize = (exp_dict["files"][i]["file_size"]*9.5367431640625e-07)
                # metadata.write(str(fsize) + "\t")
                metadata.write(str(fsize))

                # End of Metadata File Entry
                metadata.write("\n")

            i = i + 1




