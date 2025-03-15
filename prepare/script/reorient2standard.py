import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
from fsl.wrappers import fslreorient2std
from utils import _sbjname, _sesname

def reorient2standard(config, subject: int, session: int, inputname: str, outputname: str = None, input_dir: str = None, output_dir: str = None):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    assert inputname in ["bold4d", "boldwb", "fmapmg", "fmapph", "mprage"]
    
    # Get the paths
    if input_dir is None:
        input_dir = os.path.join(config['paths']['info-sampling-task-data'], sbjname, sesname, "raw")
    if output_dir is None:
        output_dir = os.path.join(config['prepare']['paths']['output'], sbjname, sesname)

    # Get the input and output names
    image2reorient = os.path.join(input_dir, inputname)
    if outputname is None:
        outputname = config['raw2prepared'][inputname]
    
    output = os.path.join(output_dir, outputname)

    # Reorient to standard
    print(f"Start reorientation to standard - {inputname}...")
    fslreorient2std(image2reorient, output)
    
    return output



if __name__ == "__main__":
    
    import yaml
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
        
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int)
    parser.add_argument("--session", type=int)
    parser.add_argument("--inputname", type=str)
    parser.add_argument("--outputname", type=str)
    parser.add_argument("--input_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    args = parser.parse_args()
    
    reorient2standard(config, args.subject, args.session, args.inputname, args.outputname, args.input_dir, args.output_dir)
