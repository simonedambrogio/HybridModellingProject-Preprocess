import yaml, os, sys
with open("config/cluster.yaml", "r") as f: 
    config = yaml.safe_load(f)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
from fsl.wrappers import fslmaths, bet, fsl_prepare_fieldmap
from reorient2standard import reorient2standard
from utils import get_dir_name

def prepare_fmap(config, subject: int, session: int, input_dir: str, output_dir: str):
    
    print("Reorienting fmapph to standard...")
    out_fmapph = reorient2standard(config, subject, session, "fmapph", input_dir=input_dir, output_dir=output_dir)
    print("Reorienting fmapmg to standard...")
    out_fmapmg = reorient2standard(config, subject, session, "fmapmg", input_dir=input_dir, output_dir=output_dir)
    
    output_dir, fmapph_name = get_dir_name(out_fmapph)
    _, fmapmg_name = get_dir_name(out_fmapmg)
    
    os.chdir(output_dir)
    
    print("BETting fmap_mag...")
    bet(fmapmg_name, fmapmg_name + '_brain')
    print("BETting expanded_func...")
    bet(fmapph_name, fmapph_name + '_brain', f=0.015)
    print("Eroding fmap_mag_brain...")
    fslmaths(fmapmg_name + '_brain').ero().ero().run(fmapmg_name + '_brain_ero')
    print("Preparing fieldmap image...")
    fsl_prepare_fieldmap(fmapph_name + '.nii.gz', fmapmg_name + '_brain_ero.nii.gz', 'fmap_rads', 1.02)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--input_dir", type=str, required=False)
    parser.add_argument("--output_dir", type=str, required=False)
    args = parser.parse_args()
    prepare_fmap(config, args.subject, args.session, args.input_dir, args.output_dir)
    