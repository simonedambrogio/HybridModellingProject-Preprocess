from .submit_slurm import *
from .submit_sge import *

def preprocess_submit(
    config, 
    subject: int, 
    session: int, 
    fsf_name: str = "design", 
    feat_name: str = "out", 
    useSpecificMask: bool = True, 
    input_dir: str = None, 
    output_dir: str = None, 
    **custom_subs):
    
    preprocess_submit_sge(
        config=config, 
        subject=subject, 
        session=session, 
        fsf_name=fsf_name, 
        feat_name=feat_name, 
        useSpecificMask=useSpecificMask, 
        input_dir=input_dir, 
        output_dir=output_dir, 
        type="fsl_sub", 
        **custom_subs
    )
