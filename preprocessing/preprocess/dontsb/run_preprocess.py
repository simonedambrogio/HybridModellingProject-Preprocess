#!/usr/bin/env python
import os
import argparse
import yaml

# Import the function directly
from preprocessing.preprocess.dontsb.feat import preprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--config_dir", type=str, required=True)
    parser.add_argument("--useSpecificMask", type=bool, default=True)
    parser.add_argument("--fsf_name", type=str, default="design.fsf")
    parser.add_argument("--feat_name", type=str, default="out")
    args = parser.parse_args()
    
    with open(os.path.join(args.config_dir, "cluster.yaml"), "r") as f: 
        config = yaml.safe_load(f)
        
    preprocess(config, args.subject, args.session, args.fsf_name, args.feat_name, args.useSpecificMask)

if __name__ == "__main__":
    main()