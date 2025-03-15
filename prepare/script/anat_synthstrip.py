import yaml, os, sys
with open("config/cluster.yaml", "r") as f: 
    config = yaml.safe_load(f)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
from fsl.wrappers import fsl_anat
import subprocess

def anat_synthstrip(anat_input, anat_output):
    
    # FSL ANAT ------------------------------------------------------------
    print("Starting fsl_anat...")
    fsl_anat(anat_input, anat_output, t="T1")
    
    anat_output_dir = anat_output + '.anat'
    t1 = os.path.join(anat_output_dir, 'T1_biascorr.nii.gz')
    t1_brain = os.path.join(anat_output_dir, 'synthstrip_biascorr_brain.nii.gz')
    brain_mask = os.path.join(anat_output_dir, 'synthstrip_biascorr_brain_mask.nii.gz')
    
    # Synthstrip ------------------------------------------------------------
    print("Starting synthstrip...")
    cmd = (
        f"/vols/Scratch/flange/bin/synthstrip-singularity "
        f"-i {t1} "
        f"-o {t1_brain} "
        f"-m {brain_mask} "
        f"--no-csf"
    )
    subprocess.run(cmd, shell=True)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--anat_input", type=str)
    parser.add_argument("--anat_output", type=str)
    args = parser.parse_args()
    anat_synthstrip(args.anat_input, args.anat_output)
