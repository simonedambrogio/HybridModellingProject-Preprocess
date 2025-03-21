from fsl.wrappers import feat
from preprocessing.preprocess.dontsb.modify_fsf import modify_fsf

def preprocess(
    config, 
    subject: int, 
    session: int, 
    fsf_name: str, 
    feat_name: str, 
    useSpecificMask: bool, 
    input_dir: str = None, 
    output_dir: str = None, 
    make_design_only: bool = False,
    **custom_subs):
     
    _, fsf_dir = modify_fsf(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir, **custom_subs)
    if not make_design_only:
        feat(fsf_dir)
