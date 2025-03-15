import os
from preprocessing.prepare.submit import prepare_struct_submit, prepare_bold4d_submit, prepare_fmap_submit, prepare_boldwb_submit
from preprocessing.prepare.dontsb.prepare_struct import prepare_struct
from preprocessing.prepare.dontsb.prepare_bold4d import prepare_bold4d
from preprocessing.prepare.dontsb.prepare_fmap import prepare_fmap
from preprocessing.prepare.dontsb.prepare_boldwb import prepare_boldwb
from preprocessing.prepare.submit import biascorrect_submit
from preprocessing.prepare.dontsb.biascorrect import _biascorrect
import shutil

def biascorrect(config, subject: int, session: int, inputname: str, input_dir: str = None, output_dir: str = None, job_id: int = None, submit: bool = False, submit_to: str = "slurm"):
    if submit:
        biascorrect_submit(config, subject, session, inputname, input_dir, output_dir, job_id, submit_to)
    else:
        _biascorrect(config, subject, session, inputname, input_dir, output_dir)

def struct(config, subject: int, session: int, input_dir: str = None, output_dir: str = None, submit: bool = False, submit_to: str = "slurm"):
    if submit:
        prepare_struct_submit(config, subject, session, input_dir, output_dir, submit_to)
    else:
        prepare_struct(config, subject, session, input_dir, output_dir)

def bold4d(config, subject: int, session: int, input_dir: str = None, output_dir: str = None, submit: bool = False, submit_to: str = "slurm"):
    if submit:
        prepare_bold4d_submit(config, subject, session, input_dir, output_dir, submit_to)
    else:
        prepare_bold4d(config, subject, session, input_dir, output_dir)

def fmap(config, subject: int, session: int, input_dir: str = None, output_dir: str = None, submit: bool = False, submit_to: str = "slurm"):
    if submit:
        prepare_fmap_submit(config, subject, session, input_dir, output_dir, submit_to)
    else:
        prepare_fmap(config, subject, session, input_dir, output_dir)

def boldwb(config, subject: int, session: int, input_dir: str = None, output_dir: str = None, submit: bool = False, submit_to: str = "slurm"):
    if submit:
        prepare_boldwb_submit(config, subject, session, input_dir, output_dir, submit_to)
    else:
        prepare_boldwb(config, subject, session, input_dir, output_dir)

# TODO: Make sure this runs after all the other steps
def cleanup(config, input_dir: str):
    # Look at files/fiolders in input_dir, and remove any file/folder that is not in the config['prepare']['files2keep'] list
    for item in os.listdir(input_dir):
        if item not in config['prepare']['files2keep']:
            if os.path.isfile(os.path.join(input_dir, item)):
                os.remove(os.path.join(input_dir, item))
            elif os.path.isdir(os.path.join(input_dir, item)):
                shutil.rmtree(os.path.join(input_dir, item))
