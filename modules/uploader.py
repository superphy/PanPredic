
from Bio import SeqIO
import os
import pandas as pd
import json
import re






#drop rows with no value and drop columns we don't need
def parse_pan(file):
    """
    :param :
        A tab delimited csv file from a panseq output
    :return: 
        A pandas dataframe with LocusID and Allele dropped as well as empty rows
    """

    df = pd.read_csv(file, sep=None)

    #drop columns we don't need
    df = df.drop(['LocusName', 'Allele'], axis=1)

    #drop rows we don't need
    df = df.dropna(axis=0, how='any')
    return df


#turn a datafarame to a list of rows lists
def pan_to_dict(df):

    """
    :param:
        A pandas dataframe from panseq
    :return: 
        A dictionary in the format for superphy to accept to add to blazegraph 
        ex. {'Some_Contig_ID':[{'START','STOP','ORIENTATION','GENE_NAME'}, {}, ....], etc}
    """

    parsed_list = []
    i = 0
    prev_ID = None
    pan_dict = {}
    for row in df.iterrows():
        index, data = row
        pan_list = data.tolist()
        row_dict = {}

        entry_list = []

        if prev_ID != pan_list[0]:
            prev_ID = pan_list[0]
            i = i + 1

        #the variable gene name here is just so that the module will work within superphy (datastruct_savvy)
        #The 'GENE_NAME' actually refers to the Locus Name and should be renamed to reflect this

        row_dict['GENE_NAME'] = pan_list[0]
        row_dict['GENOME'] = pan_list[1]
        row_dict['START'] = pan_list[2]
        row_dict['STOP'] = pan_list[3]
        row_dict["PanID"] = i
        contig_name = pan_list[4]

        if contig_name in pan_dict:
            pan_dict[contig_name].append(row_dict)

        else:
            pan_dict[contig_name] = [row_dict]

    return pan_dict

def get_sequence_dict(file):
    """
    :param:
        a fasta file
    :return: 
        A dictionary in the format {header:sequence, header:sequence, ....}
    """

    sequence_dict = {}
    for record in SeqIO.parse(file, "fasta"):
        sequence_dict[record.description] = str(record.seq)

    return sequence_dict

''''

def merge_dicts(sequence_dict, pan_dict):
    """
    :param:
        a fasta file
    :return: 
        A dictionary in the format {header:sequence, header:sequence, ....}
    """
    for record in pan_dict:
        for panregion in pan_dict[record]:
            for header in sequence_dict:

'''


def contig_name_parse(pan_contig):
    """
    The panseq contig name is unhelpful
    :param:
        a contig named by panseq
    :return: 
        the basename of the contig
    """

    m = re.search('(?<=\|)(.*?)(?=_E)', pan_contig)
    # print(m.group(0))
    m = re.search('(?<=\|).+', m.group(0))

    return m.group(0)

def json_dump(file, dict):
    with open(file, 'w') as fp:
        json.dump(dict, fp)


def json_load(file):
    with open(file) as fp:
        data = json.load(fp)

    return data


def workflow(file):

    df = parse_pan(file)
    pan_dict = pan_to_dict(df)
    json_dump('pandump.json', pan_dict)


#generates a hash for a file
def generate_hash(filename):

    """
    :param:
        a file 
    :return: 
        sha1 hash
    """

    from hashlib import sha1
    # the 'b' isn't needed less you run this on Windows
    with open(filename, 'rb') as f:
    #  we apply a sort func to make sure the contents are the same,        # regardless of order
        return sha1(str(sorted(f.readlines())).encode('utf-8')).hexdigest()


def main(dr):

    """
    :param:
        directory of fasta files
    :return: 
        Dictionary in format {contig_name: sha1hash} for each contig in fasta files
    """

    from Bio import SeqIO
    d = {}
    for f in os.listdir(dr):
        h = generate_hash(dr + f)
        for record in SeqIO.parse(open(dr + f), "fasta"):
            d[record.id] = h
    json_dump('hash_dict.json', d)



