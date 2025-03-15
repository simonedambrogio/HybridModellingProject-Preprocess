import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import preprocessing.prepare as prepare

if __name__ == "__main__":
    import yaml
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int)
    parser.add_argument("--session", type=int)
    args = parser.parse_args()

    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
        
    prepare.fmap(config, args.subject, args.session, submit=True, submit_to="sge")
