import os, sys, shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocessing.utils import _sbjname, _sesname

def main(config, subject, session):
    file_from = os.path.join(
        config['prepare']['paths']['input'], _sbjname(subject), _sesname(session), 
        "prepared", "struct_brain.anat", "synthstrip_biascorr_brain.nii.gz")
    
    file_from = os.path.join(config['paths']["data"], "fsl", "data", str(subject), str(session), "first-level", "funcmask.nii.gz")
    
    file_to = os.path.join(
        config['prepare']['paths']['output'], _sbjname(subject), _sesname(session), 
        "funcmask.nii.gz")
    shutil.copy(file_from, file_to)

if __name__ == "__main__":
    import argparse, yaml
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int)
    parser.add_argument("--session", type=int)
    args = parser.parse_args()
    
    with open("config/cluster.yaml", "r") as f:
        config = yaml.safe_load(f)

    subjects = range(1, 21) if args.subject is None else [args.subject]
    sessions = [1, 2, 3, 4] if args.session is None else [args.session]
    
    for subject in subjects:
        for session in sessions:
            print(f"\n\033[92mCopying funcmask for subject {subject} session {session}\033[0m")
            main(config, subject, session)
