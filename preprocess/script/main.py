from modify_fsf import modify_fsf
from preprocess import preprocess
import argparse

if __name__ == "__main__":
    
    import yaml
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--useSpecificMask", type=bool, default=True)
    parser.add_argument("--fsf_name", type=str, default="design.fsf")
    parser.add_argument("--feat_name", type=str, default="out")
    args = parser.parse_args()
    
    _, fsf_dir = modify_fsf(config, args.subject, args.session, args.useSpecificMask, args.fsf_name, args.feat_name)
    preprocess(fsf_dir)
    