import os
from fsl.wrappers import fslmaths, bet, fsl_prepare_fieldmap
from preprocessing.utils import get_dir_name
from preprocessing.prepare.dontsb.reorient2standard import _reorient2standard

def prepare_fmap(config, subject: int, session: int, input_dir: str, output_dir: str):
    
    print("Reorienting fmapph to standard...")
    out_fmapph = _reorient2standard(config, subject, session, "fmapph", input_dir=input_dir, output_dir=output_dir)
    print("Reorienting fmapmg to standard...")
    out_fmapmg = _reorient2standard(config, subject, session, "fmapmg", input_dir=input_dir, output_dir=output_dir)
    
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