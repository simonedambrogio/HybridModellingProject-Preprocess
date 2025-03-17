import sys, os        
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import preprocessing.prepare as prepare

def main(config, subject, session, step, submit, submit_to):
    
    assert step in ["all", "bold4d", "struct", "boldwb", "fmap"], "Step must be one of: all, bold4d, struct, boldwb, fmap"
    assert session in [1,2,3,4], "Session must be one of: 1, 2, 3, 4"
    
    if step in ["all", "bold4d"]:
        prepare.bold4d(config, subject, session, submit=submit, submit_to=submit_to)

    if session in [1,3]:
        if step in ["all", "struct"]:
            prepare.struct(config, subject, session, submit=submit, submit_to=submit_to)
        if step in ["all", "boldwb"]:
            prepare.boldwb(config, subject, session, submit=submit, submit_to=submit_to)
        if step in ["all", "fmap"]:
            prepare.fmap(config, subject, session, submit=submit, submit_to=submit_to)

if __name__ == "__main__":      
    import argparse, yaml
    
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=False)
    parser.add_argument("--step", default="all", type=str, required=False)
    parser.add_argument("--submit_to", type=str, required=False, choices=["slurm", "sge"])
    args = parser.parse_args()
    
    submit = True if args.submit_to is not None else False
    
    sessions = [1,3] if args.session is None else [args.session]
    for session in sessions:
        main(config, args.subject, session, args.step, submit, args.submit_to)
