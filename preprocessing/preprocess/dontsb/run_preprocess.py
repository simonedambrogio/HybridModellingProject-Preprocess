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
    parser.add_argument("--make_design_only", action="store_true", help="If True, only the design will be made, but the feat will not be run")
    parser.add_argument("--custom_subs", type=dict, default={})
    args = parser.parse_args()
    
    with open(os.path.join(args.config_dir, "cluster.yaml"), "r") as f: 
        config = yaml.safe_load(f)
        
    if args.custom_subs is not None:
        preprocess(config, args.subject, args.session, args.fsf_name, args.feat_name, args.useSpecificMask, args.make_design_only, args.custom_subs)
    else:
        preprocess(config, args.subject, args.session, args.fsf_name, args.feat_name, args.useSpecificMask, args.make_design_only)

if __name__ == "__main__":
    main()