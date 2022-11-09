# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_dataset.ipynb.

# %% auto 0
__all__ = ['read_source_ref', 'download_read_set', 'read_own_set', 'get_translated_test_set', 'read_tsv_set']

# %% ../nbs/02_dataset.ipynb 5
import sys
def read_source_ref(source_path,ref_path):
    """Read the testset into two arrays and return them"""
    source_lines = []
    reference_lines = []
    with open(source_path) as source_fh, open(ref_path) as reference_fh :
        for (source_line,reference_line) in zip(source_fh,reference_fh):
            source_line = source_line.rstrip()
            source_lines.append(source_line)
            reference_line = reference_line.rstrip()
            reference_lines.append(reference_line) 
    return source_lines, reference_lines

# %% ../nbs/02_dataset.ipynb 6
from pathlib import Path
import sys
import os
from sacrebleu.utils import download_test_set
from shutil import copy
def download_read_set(base_path,source_language_code,target_language_code,test_set_name):
    """Downloads data set if it is not cached. Return source and reference arrays."""
    language_pair = source_language_code+"-"+target_language_code
    output_path = base_path+source_language_code+"_"+target_language_code+"/"+test_set_name
    source_path = output_path+"/src."+language_pair+"."+source_language_code
    ref_path = output_path+"/ref."+language_pair+"."+target_language_code

    # Download source and language files if they do not exist yet
    source_file = Path(source_path)
    ref_file = Path(ref_path)
    if not source_file.exists() and not ref_file.exists():
        file_paths = download_test_set(test_set_name,language_pair)
        # Create the output path if it doesn't already exist
        os.makedirs(output_path,exist_ok=True)
        # Backing up the source and reference files to the output folder 
        copy(file_paths[0],source_path)
        copy(file_paths[1],ref_path)
    
    return read_source_ref(source_path,ref_path)

# %% ../nbs/02_dataset.ipynb 7
from pathlib import Path
import os
import errno

def read_own_set(base_path,source_language_code,target_language_code,test_set_name,date=''):
    """Reads already present non-sacrebleu test set. Return source and reference arrays."""
    language_pair = source_language_code+"-"+target_language_code
    if date != '':
        output_path = base_path+source_language_code+"_"+target_language_code+"/"+date+"/"+test_set_name
    else:
        output_path = base_path+source_language_code+"_"+target_language_code+"/"+test_set_name
    source_path = output_path+"/src."+language_pair+"."+source_language_code
    ref_path = output_path+"/ref."+language_pair+"."+target_language_code

    # Download source and language files if they do not exist yet
    source_file = Path(source_path)
    ref_file = Path(ref_path)
    if not source_file.exists():
        raise FileNotFoundError(errno.ENOENT,os.strerr(errno.ENOENT),source_path) 
    if not ref_file.exists():
        raise FileNotFoundError(errno.ENOENT,os.strerr(errno.ENOENT),ref_path) 
    
    return read_source_ref(source_path,ref_path)

# %% ../nbs/02_dataset.ipynb 10
import sys
def get_translated_test_set(base_path,sourcelang,targetlang,mtengine,test_set_name,test_date):
    """Read MT hypothesis translations for specified MT engine"""
    target_lines = []
    langpair = sourcelang+"-"+targetlang
    output_filename = "hyp_"+mtengine+"."+langpair+"."+targetlang
    from pathlib import Path
    translate_file = Path(base_path+sourcelang+"_"+targetlang+"/"+test_date+"/"+test_set_name+"/"+output_filename)
    if translate_file.exists():
        with translate_file.open() as target_file:
            for target_line in target_file:
                target_line = target_line.rstrip()
                target_lines.append(target_line)
        return target_lines
    else:
        raise FileNotFoundError(errno.ENOENT,os.strerror(errno.ENOENT),translate_file) 

# %% ../nbs/02_dataset.ipynb 12
from pathlib import Path
import os
import errno

def read_tsv_set(tsv_file):
    """Reads complete evaluation set from TSV file containing source, hypothesis and reference"""
    sources = []
    hypotheses = []
    references = []
    line_counter = 0
    with open(tsv_file,"r") as tsv_fh:
        for tsv_line in tsv_fh:
            line_counter += 1
            tsv_line = tsv_line.rstrip()
            source, hypothesis, reference = tsv_line.split('\t')[:3]
            if not source:
                raise ValueError('source string is empty; line:'+str(line_counter))
            if not hypothesis:
                raise ValueError('hypothesis string is empty; line:'+str(line_counter))
            if not reference:
                raise ValueError('reference string is empty; line:'+str(line_counter))
            sources.append(source)
            hypotheses.append(hypothesis)
            references.append(reference)
    return sources,hypotheses,references