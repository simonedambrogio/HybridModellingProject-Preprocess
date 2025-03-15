from preprocessing.preprocess.dontsb import preprocess as preprocess_dontsb
from preprocessing.preprocess.submit import preprocess_submit

def preprocess(config: dict, subject: int, session: int, fsf_name: str = "design.fsf", feat_name: str = "out", useSpecificMask: bool = True, input_dir: str = None, output_dir: str = None, submit: bool = False, submit_to: str = "slurm", type: str = "sge"):
    if submit:
        preprocess_submit(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir, submit_to, type)
    else:
        preprocess_dontsb(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir)
