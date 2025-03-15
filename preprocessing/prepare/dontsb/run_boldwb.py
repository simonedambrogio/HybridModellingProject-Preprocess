#!/usr/bin/env python
import os
import argparse
import yaml

# Import the function directly
from preprocessing.prepare.dontsb.prepare_boldwb import prepare_boldwb

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--config_dir", type=str, required=True)
    parser.add_argument("--input_dir", type=str, required=False)
    parser.add_argument("--output_dir", type=str, required=False)
    args = parser.parse_args()
    
    with open(os.path.join(args.config_dir, "cluster.yaml"), "r") as f: 
        config = yaml.safe_load(f)
        
    prepare_boldwb(config, args.subject, args.session, args.input_dir, args.output_dir)

if __name__ == "__main__":
    main() 