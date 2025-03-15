import os
import argparse
from fsl.wrappers import fslmaths, bet, fsl_prepare_fieldmap
from preprocessing.utils import _sbjname, _sesname
from preprocessing.prepare.dontsb.reorient2standard import _reorient2standard

def _prepare_wbrain_fmap(config, subject: int, session: int, input_dir: str, output_dir: str):
    print("Reorienting boldwb to standard...")
    _reorient2standard(config, subject, session, "boldwb", input_dir=input_dir, output_dir=output_dir)
    print("Reorienting fmapph to standard...")
    _reorient2standard(config, subject, session, "fmapph", input_dir=input_dir, output_dir=output_dir)
    print("Reorienting fmapmg to standard...")
    _reorient2standard(config, subject, session, "fmapmg", input_dir=input_dir, output_dir=output_dir)
    
    if output_dir is None:
        sbjname = _sbjname(subject)
        sesname = _sesname(session)
        output_dir = os.path.join(config['prepare']['paths']['output'], sbjname, sesname)
    
    os.chdir(output_dir)
    
    print("BETting fmap_mag...")
    bet('fmap_mag', 'fmap_mag_brain')
    print("BETting expanded_func...")
    bet('expanded_func', 'expanded_func_brain', f=0.015)
    print("Eroding fmap_mag_brain...")
    fslmaths('fmap_mag_brain').ero().ero().run('fmap_mag_brain_ero')
    print("Preparing fieldmap image...")
    fsl_prepare_fieldmap('fmap_phase.nii.gz', 'fmap_mag_brain_ero', 'fmap_rads', 1.02)

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
    _prepare_wbrain_fmap(config, args.subject, args.session, args.input_dir, args.output_dir)
    