__author__ = 'AJ'


def tsv_to_json(metadata):
    """
    This function will convert the metadata file to a json object for upload to CoGe

    :param metadata: A metadata.txt in TSV form
    :return: A json object of the metadata file
    """
    import csv
    # save the json output as emp.json

    genome_id = str(25577)
    jsfile = file('test.json', 'w')
    jsfile.write('[\r\n')

    with open(metadata,'r') as f:
        headings = next(f)
        headings = headings.replace('\n','')
        headings = headings.split("\t")



        next(f) # skip headings
        reader = csv.reader(f,delimiter='\t')



         # get the total number of rows excluded the heading
        row_count = len(list(reader))
        ite = 0

        # back to first position
        f.seek(0)
        next(f) # skip headings

        for headings in reader:

            ite+= 1

            jsfile.write('\t{\r\n')


            Name = '\t\t\"name\": \"' + headings[0] + '\",\r\n'
            Experiment_Name = '\t\t\"Experiment_Name\": \"' + headings[1] + '\",\r\n'
            Description = '\t\t\"Description\": \"' + headings[2] + '\",\r\n'
            Assay = '\t\t\"Assay\": \"' + headings[3] + '\",\r\n'
            Replicate = '\t\t\"Replicate\": \"' + headings[4] + '\",\r\n'
            Cell_Type = '\t\t\"Cell Type\": \"' + headings[5] + '\",\r\n'
            Bio_Sample = '\t\t\"Bio Sample\": \"' + headings[6] + '\",\r\n'
            Target = '\t\t\"Target\": \"' + headings[7] + '\",\r\n'
            Assembly = '\t\t\"Assembly\": \"' + headings[8] + '\",\r\n'
            Lab = '\t\t\"Lab\": \"' + headings[9] + '\",\r\n'
            Date = '\t\t\"Date\": \"' + headings[10] + '\",\r\n'
            Version = '\t\t\"version\": \"' + headings[11] + '\",\r\n'
            Source = '\t\t\"source_name\": \"' + headings[12] + '\",\r\n'
            Download_Link = '\t\t\"Download Link\": \"' + headings[13] + '\",\r\n'
            Source_Link = '\t\t\"Source Link\": \"' + headings[14] + '\",\r\n'
            Sequencer = '\t\t\"Sequencer\": \"' + headings[15] + '\",\r\n'
            Run_Type = '\t\t\"Run Type\": \"' + headings[16] + '\",\r\n'
            File_Type = '\t\t\"File_Type\": \"' + headings[17] + '\",\r\n'
            Biosample_term_id = '\t\t\"Biosample Term ID\": \"' + headings[18] + '\",\r\n'
            File_Size = '\t\t\"File Size\": \"' + headings[19] + '\"\r\n'
            Genome_Id = '\t\t\"genome_id\": \"' + genome_id + '\"\r\n'

            jsfile.write(Name)
            jsfile.write(Experiment_Name)
            jsfile.write(Description)
            jsfile.write(Assay)
            jsfile.write(Replicate)
            jsfile.write(Cell_Type)
            jsfile.write(Bio_Sample)
            jsfile.write(Target)
            jsfile.write(Assembly)
            jsfile.write(Lab)
            jsfile.write(Date)
            jsfile.write(Version)
            jsfile.write(Source)
            jsfile.write(Download_Link)
            jsfile.write(Source_Link)
            jsfile.write(Sequencer)
            jsfile.write(Run_Type)
            jsfile.write(File_Type)
            jsfile.write(Biosample_term_id)
            jsfile.write(File_Size)
            jsfile.write(Genome_Id)



            jsfile.write('\t}')

            # omit comma for last row item
            if ite < row_count:
                jsfile.write(',\r\n')

            jsfile.write('\r\n')

    jsfile.write(']')
    jsfile.close()



tsv_to_json("bam_metadata_encode.txt")

