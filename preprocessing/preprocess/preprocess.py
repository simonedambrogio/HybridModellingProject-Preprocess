from preprocessing.preprocess.dontsb import preprocess as preprocess_dontsb
from preprocessing.preprocess.submit import preprocess_submit

def preprocess(
    config: dict, 
    subject: int, 
    session: int, 
    fsf_name: str = "design.fsf", 
    feat_name: str = "out", 
    useSpecificMask: bool = True, 
    input_dir: str = None, 
    output_dir: str = None, 
    make_design_only: bool = False, 
    submit: bool = False, 
    **custom_subs):
    
    
    if submit:
        preprocess_submit(
            config, 
            subject=subject, 
            session=session, 
            fsf_name=fsf_name, 
            feat_name=feat_name, 
            useSpecificMask=useSpecificMask, 
            input_dir=input_dir, 
            output_dir=output_dir, 
            **custom_subs)
    else:
        preprocess_dontsb(
            config=config, 
            subject=subject, 
            session=session, 
            fsf_name=fsf_name, 
            feat_name=feat_name, 
            useSpecificMask=useSpecificMask, 
            input_dir=input_dir, 
            output_dir=output_dir, 
            make_design_only=make_design_only, 
            **custom_subs)
