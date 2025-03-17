import os, shutil
from preprocessing.prepare.dontsb.reorient2standard import _reorient2standard
from preprocessing.prepare.dontsb.anat_synthstrip import _anat_synthstrip
from preprocessing.utils import _sbjname, _sesname

def prepare_struct(config, subject: int, session: int, input_dir: str, output_dir: str):
    
    # Check if the input file exists ----------------------------------------------
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    if input_dir is None:
        input_dir = os.path.join(config['prepare']['paths']['input'], sbjname, sesname, "raw")
    input_file = os.path.join(input_dir, "mprage.nii")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"mprage.nii not found in {input_dir}")
    
    # Reorient2Standard
    anat_input = _reorient2standard(config, subject, session, "mprage", input_dir=input_dir, output_dir=output_dir)
    
    # FSL Anat and Synthstrip
    anat_output = os.path.join(output_dir, "struct_brain")
    _anat_synthstrip(anat_input, anat_output)
    
    # Copy synthstrip_biascorr_brain to prepare directory
    anat_output_dir = os.path.join(output_dir, "struct_brain.anat")
    file_from = os.path.join(anat_output_dir, "synthstrip_biascorr_brain.nii.gz")
    file_to = os.path.join(output_dir, "synthstrip_biascorr_brain.nii.gz")
    shutil.copy(file_from, file_to)
    
    # Remove anat_output directory
    shutil.rmtree(anat_output_dir)
    