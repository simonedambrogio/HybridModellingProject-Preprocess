import os
from preprocessing.utils import _sbjname, _sesname
from preprocessing.sge import SGE
from preprocessing.preprocess.dontsb import modify_fsf

def preprocess_submit_sge(config: dict, subject: int, session: int, fsf_name: str, feat_name: str, useSpecificMask: bool = True, input_dir: str = None, output_dir: str = None, type = "sge", **custom_subs):
    
    assert type in ["sge", "fsl_sub"], "Type must be either 'sge' or 'fsl_sub'"
    
    _, fsf_dir = modify_fsf(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir, **custom_subs)
    
    sbjname = _sbjname(subject)
    sesname = _sesname(session)

    job = SGE(
        job_name=f"preprocess_{sbjname}_{sesname}",
        memory="18G",
        logdir=os.path.join(config["preprocess"]["paths"]["output"], sbjname, sesname, "logs"),
        conda_env="fsl_sub",
        fsl_dir=config["paths"]["FSLDIR"],
        type=type
    )
    
    job.submit(command=f"feat {fsf_dir}", type=type, create_script=False)
