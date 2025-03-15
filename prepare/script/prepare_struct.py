import os, sys, shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
from reorient2standard import reorient2standard
from anat_synthstrip import anat_synthstrip

def prepare_struct(config, subject: int, session: int, input_dir: str, output_dir: str):
    
    # Reorient2Standard
    anat_input = reorient2standard(config, subject, session, "mprage", input_dir=input_dir, output_dir=output_dir)
    
    # FSL Anat and Synthstrip
    anat_output = os.path.join(output_dir, "struct_brain")
    anat_synthstrip(anat_input, anat_output)
    
    # Copy synthstrip_biascorr_brain to prepare directory
    anat_output_dir = os.path.join(output_dir, "struct_brain.anat")
    file_from = os.path.join(anat_output_dir, "synthstrip_biascorr_brain.nii.gz")
    file_to = os.path.join(output_dir, "synthstrip_biascorr_brain.nii.gz")
    shutil.copy(file_from, file_to)
    
    # Remove anat_output directory
    shutil.rmtree(anat_output_dir)
    
if __name__ == "__main__":
    
    import yaml
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--input_dir", type=str, required=False)
    parser.add_argument("--output_dir", type=str, required=False)
    args = parser.parse_args()
    
    prepare_struct(config, args.subject, args.session, args.input_dir, args.output_dir)