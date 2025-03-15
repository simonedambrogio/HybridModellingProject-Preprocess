import os
import argparse
from ..utils import _sbjname, _sesname
from simple_slurm import Slurm

# TODO: Test on OOD cluster
def preprocess_submit_slurm(config: dict, subject: int, session: int, fsf_name: str = None, feat_name: str = None, useSpecificMask: bool = False, input_dir: str = None, output_dir: str = None):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(config["preprocess"]["paths"]["output"], sbjname, sesname, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create a Slurm object with the job parameters
    slurm = Slurm(
        job_name=f"preprocess_{sbjname}_{sesname}",
        partition="short",  # Equivalent to queue in SGE
        time="06:00:00",    # Runtime
        mem="20G",          # Memory requirement
        output=os.path.join(logs_dir, f"preprocess_{sbjname}_{sesname}.out"),
        error=os.path.join(logs_dir, f"preprocess_{sbjname}_{sesname}.err")
    )
    
    # Build command to run the Python module
    cmd = (
        f"python -m preprocessing.preprocess.dontsb.run_preprocess "
        f"--subject {subject} "
        f"--session {session} "
        f"--fsf_name {fsf_name} "
        f"--feat_name {feat_name} "
        f"--useSpecificMask {useSpecificMask} "
        f"--config_dir {config['paths']['config_dir']} "
        f"--input_dir {input_dir} "
        f"--output_dir {output_dir} "
    )
    
    # Submit the job
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"Preprocess job ID: {job_id}")
    
    return job_id
    