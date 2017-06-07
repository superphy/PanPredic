from app.modules.PanPredic.modules.pan_run import panseq
from app.modules.PanPredic.modules.uploader import workflow
from app.modules.PanPredic.modules.conf_gen import generate_conf
from app.modules.PanPredic.definitions import PAN_RESULTS, NOVEL_RESULTS

def pan(args_dict):

    # (1) generate conf files
    query_dict = generate_conf(args_dict['i'])

    # (2) run panseq
    panseq(query_dict)

    # (3) Parse panseq results
    results_pickle = workflow(PAN_RESULTS + '/pan_genome.txt', PAN_RESULTS + '/coreGenomeFragments.fasta')

    return results_pickle

    # (4) upload pan data to blazegraph

    # (5) analyze pan data
'''
dict = {}
dict['genomes'] = '/home/james/backend/app/modules/PanPredic/tests/data/filteredgenomes'

pan(dict)
'''