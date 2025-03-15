import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
from utils import _sbjname, _sesname
from prepare import _struct, _brain4d, _brainwb, _fmap, _cleanup


def prepare(config, subject: int, session: int, submit_to: str = "slurm"):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)

    # Get the paths
    rawdata_dir = os.path.join(config['paths']['info-sampling-task-data'], sbjname, sesname, "raw")
    prepare_dir = os.path.join(config['paths']['preprocess'], "prepare")
    output_dir = os.path.join(prepare_dir, "output", sbjname, sesname)

    # Create the prepared directory
    print(f"Create the prepared directory - {output_dir}...")
    os.makedirs(output_dir, exist_ok=True)

    # Prepare Images ----
    _brain4d(config, subject, session, rawdata_dir, output_dir, submit=True)
    if session in [1,3]:
        _struct(config, subject, session, rawdata_dir, output_dir, submit=True)
        _brainwb(config, subject, session, rawdata_dir, output_dir, submit=False)
        _fmap(config, subject, session, rawdata_dir, output_dir, submit=False)

    # Clean up the prepared directory
    _cleanup(config, output_dir)

if __name__ == "__main__":
    import yaml
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int)
    parser.add_argument("--session", type=int)
    args = parser.parse_args()
    
    prepare(config, args.subject, args.session)
