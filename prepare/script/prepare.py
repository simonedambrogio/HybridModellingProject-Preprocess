import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from submit import prepare_struct_submit, prepare_bold4d_submit, prepare_fmap_submit, prepare_boldwb_submit
from prepare_struct import prepare_struct
from prepare_bold4d import prepare_bold4d
from prepare_fmap import prepare_fmap
from prepare_boldwb import prepare_boldwb
import shutil

def _struct(config, subject: int, session: int, input_dir: str, output_dir: str, submit: bool, submit_to: str = "slurm"):
    if submit:
        prepare_struct_submit(config, subject, session, input_dir, output_dir, submit_to)
    else:
        prepare_struct(config, subject, session, input_dir, output_dir)

def _bold4d(config, subject: int, session: int, input_dir: str, output_dir: str, submit: bool, submit_to: str = "slurm"):
    if submit:
        prepare_bold4d_submit(config, subject, session, input_dir, output_dir, submit_to)
    else:
        prepare_bold4d(config, subject, session, input_dir, output_dir)

def _fmap(config, subject: int, session: int, input_dir: str, output_dir: str, submit: bool, submit_to: str = "slurm"):
    if submit:
        prepare_fmap_submit(config, subject, session, input_dir, output_dir, submit_to)
    else:
        prepare_fmap(config, subject, session, input_dir, output_dir)

def _boldwb(config, subject: int, session: int, input_dir: str, output_dir: str, submit: bool, submit_to: str = "slurm"):
    if submit:
        prepare_boldwb_submit(config, subject, session, input_dir, output_dir, submit_to)
    else:
        prepare_boldwb(config, subject, session, input_dir, output_dir)

# TODO: Make sure this runs after all the other steps
def _cleanup(config, input_dir: str):
    # Look at files/fiolders in input_dir, and remove any file/folder that is not in the config['prepare']['files2keep'] list
    for item in os.listdir(input_dir):
        if item not in config['prepare']['files2keep']:
            if os.path.isfile(os.path.join(input_dir, item)):
                os.remove(os.path.join(input_dir, item))
            elif os.path.isdir(os.path.join(input_dir, item)):
                shutil.rmtree(os.path.join(input_dir, item))

def _prepare(config, subject: int, session: int, input_dir: str, output_dir: str, submit: bool, submit_to: str = "slurm"):
    _struct(config, subject, session, input_dir, output_dir, submit, submit_to)
    _bold4d(config, subject, session, input_dir, output_dir, submit, submit_to)
    _fmap(config, subject, session, input_dir, output_dir, submit, submit_to)
    _boldwb(config, subject, session, input_dir, output_dir, submit, submit_to)
    _cleanup(config, input_dir)