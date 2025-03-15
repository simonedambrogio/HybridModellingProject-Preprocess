import os, sys, shutil
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocessing.utils import _sbjname, _sesname

def main(config, subject, session):
    
    for fname in config['prepare']['files2keep']:
        if os.path.exists(os.path.join(
            config['prepare']['paths']['output'], _sbjname(subject), _sesname(session), fname)):
            print(f"\033[93m{fname} already exists for subject {subject} session {session}\033[0m")
            continue
        
        file_from = os.path.join(
            config['prepare']['paths']['output'], _sbjname(subject), _sesname(session-1), 
            fname)
        file_to = os.path.join(
            config['prepare']['paths']['output'], _sbjname(subject), _sesname(session), 
            fname)
        os.symlink(file_from, file_to)
        print(f"\033[92m{fname} symbolic link created for subject {subject} session {session}\033[0m")

if __name__ == "__main__":
    import argparse, yaml
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int)
    parser.add_argument("--session", type=int)
    args = parser.parse_args()
    
    with open("config/cluster.yaml", "r") as f:
        config = yaml.safe_load(f)

    subjects = range(1, 21) if args.subject is None else [args.subject]
    sessions = [2, 4] if args.session is None else [args.session]
    
    for subject in subjects:
        for session in sessions:
            print(f"\n\033[92mCopying func_mask for subject {subject} session {session}\033[0m")
            main(config, subject, session)
