import yaml, os, sys
with open("config/cluster.yaml", "r") as f: 
    config = yaml.safe_load(f)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
from fsl.wrappers import bet
from reorient2standard import reorient2standard
from utils import get_dir_name

def prepare_boldwb(config, subject: int, session: int, input_dir: str, output_dir: str):
    print("Reorienting boldwb to standard...")
    out = reorient2standard(config, subject, session, "boldwb", input_dir=input_dir, output_dir=output_dir)
    
    print("BETting expanded_func...")
    os.chdir(output_dir)
    output_dir, output_name = get_dir_name(out)
    bet(output_name, output_name + '_brain', f=0.015)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--input_dir", type=str, required=False)
    parser.add_argument("--output_dir", type=str, required=False)
    args = parser.parse_args()
    prepare_boldwb(config, args.subject, args.session, args.input_dir, args.output_dir)
    