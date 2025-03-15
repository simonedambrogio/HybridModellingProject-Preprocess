import sys, os        
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import preprocessing.prepare as prepare

def main(config, subject, session, submit, submit_to):
    prepare.bold4d(config, subject, session, submit=submit, submit_to=submit_to)
    if session in [1,3]:
        prepare.struct(config, subject, session, submit=submit, submit_to=submit_to)
        prepare.boldwb(config, subject, session, submit=submit, submit_to=submit_to)
        prepare.fmap(config, subject, session, submit=submit, submit_to=submit_to)

if __name__ == "__main__":      
    import argparse, yaml
    
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=False)
    parser.add_argument("--submit_to", type=str, required=False, default="slurm", choices=["slurm", "sge"])
    args = parser.parse_args()
    
    submit = True if args.submit_to is not None else False
    
    sessions = range(1, 5) if args.session is None else [args.session]
    for session in sessions:
        main(config, args.subject, session, submit, args.submit_to)
