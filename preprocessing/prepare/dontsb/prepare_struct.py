import os, shutil
from preprocessing.prepare.dontsb.reorient2standard import _reorient2standard
from preprocessing.prepare.dontsb.anat_synthstrip import _anat_synthstrip

def prepare_struct(config, subject: int, session: int, input_dir: str, output_dir: str):
    
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
    