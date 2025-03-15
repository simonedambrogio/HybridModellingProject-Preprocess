from .submit_slurm import *
from .submit_sge import *

def preprocess_submit(config, subject: int, session: int, fsf_name: str = "design", feat_name: str = "out", useSpecificMask: bool = True, input_dir: str = None, output_dir: str = None, submit: str = "slurm", type = "sge"):
    assert submit in ["slurm", "sge"], f"Submit method {submit} not supported"
    assert type in ["sge", "fsl_sub"], "Type must be either 'sge' or 'fsl_sub'"
    if submit == "slurm":
        preprocess_submit_slurm(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir)
    elif submit == "sge":
        preprocess_submit_sge(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir, type)
    else:
        raise ValueError(f"Submit method {submit} not supported")
