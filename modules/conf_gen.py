from app.modules.PanPredic.definitions import ROOT_DIR, PAN_RESULTS, NOVEL_RESULTS
from app.modules.PanPredic.modules.queries import check_panseq
from app.modules.PanPredic.modules.pan_run import build_pan




# TODO: edit file locations of programs

def gen_novel(genome_files):

    with open(ROOT_DIR + '/panseq_novel_pangenome.conf', 'wb') as f:
        f.writelines([b'queryDirectory   ' + genome_files.encode() + b'\n',
                    b'referenceDirectory '	+ ROOT_DIR.encode() + b'/Data \n',
                    b'baseDirectory  ' + NOVEL_RESULTS.encode() + b'\n',
                    b'numberOfCores	4 \n',
                    b'mummerDirectory	/home/james/pan_genome/MUMmer3.23/ \n',
                    b'blastDirectory	/home/james/pan_genome/ncbi-blast-2.6.0+/bin/ \n',
                    b'minimumNovelRegionSize	500 \n',
                    b'novelRegionFinderMode	no_duplicates \n',
                    b'muscleExecutable	/home/james/pan_genome/muscle3.8.31_i86linux64 \n',
                    b'fragmentationSize	500 \n',
                    b'percentIdentityCutoff	90 \n',
                    b'runMode	novel \n',
                    b'overwrite 1 \n',
                      b'sha1 1 \n'])
        return ROOT_DIR + '/panseq_novel_pangenome.conf'


def gen_match(genome_files):

    settings_list = [b'queryDirectory   ' + genome_files.encode() + b'\n',
                    #'queryFile  ' + ROOT_DIR + '/PanGenomeRef/coreGenomeFragments.fasta',
                    b'baseDirectory  '  +  PAN_RESULTS.encode() + b'\n',
                    b'numberOfCores	4 \n',
                    b'mummerDirectory	/home/james/pan_genome/MUMmer3.23/ \n',
                    b'blastDirectory	/home/james/pan_genome/ncbi-blast-2.6.0+/bin/ \n',
                    b'minimumNovelRegionSize	500 \n',
                    b'muscleExecutable	/home/james/pan_genome/muscle3.8.31_i86linux64 \n',
                    b'novelRegionFinderMode	no_duplicates \n',
                    b'fragmentationSize	500 \n',
                    b'percentIdentityCutoff	90 \n',
                    b'coreGenomeThreshold   1000000000 \n',
                    b'runMode	pan \n',
                    b'nameOrId	id \n',
                    b'overwrite 1 \n',
                     b'sha1 1 \n']

    pan_list = check_panseq()


    if pan_list:
        settings_list.insert(1, b'queryFile  ' +  ROOT_DIR.encode() +  b'/Data/PanGenomeRegions.fasta\n')




    with open(ROOT_DIR + '/panseq_pan_pangenome.conf', 'wb') as f:
        f.writelines(settings_list)
        return ROOT_DIR + '/panseq_pan_pangenome.conf'

#driver function generates both necessary conf files
def generate_conf(genome_files):

    query_dict = {}

    query_dict['novel'] = gen_novel(genome_files)
    query_dict['match'] = gen_match(genome_files)

    return query_dict

