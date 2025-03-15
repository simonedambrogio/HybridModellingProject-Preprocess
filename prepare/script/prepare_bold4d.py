import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
from reorient2standard import reorient2standard
from biascorrect import biascorrect

def prepare_bold4d(config, subject: int, session: int, input_dir: str, output_dir: str):
    
    # Reorient2Standard
    print("Reorienting bold4d to standard...")
    reorient2standard(config, subject, session, "bold4d", input_dir=input_dir, output_dir=output_dir)
    
    # Bias Correction
    print("Bias correcting bold4d...")
    input_dir = output_dir
    biascorrect(config, subject, session, "func", input_dir, output_dir)

if __name__ == "__main__":
    
    import yaml
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--input_dir", type=str, required=False)
    parser.add_argument("--output_dir", type=str, required=False)
    args = parser.parse_args()
    prepare_bold4d(config, args.subject, args.session, args.input_dir, args.output_dir)
