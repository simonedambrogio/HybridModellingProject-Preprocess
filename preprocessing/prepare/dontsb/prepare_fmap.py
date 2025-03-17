import os
from fsl.wrappers import fslmaths, bet, fsl_prepare_fieldmap
from preprocessing.utils import get_dir_name
from preprocessing.prepare.dontsb.reorient2standard import _reorient2standard
from preprocessing.utils import _sbjname, _sesname

def prepare_fmap(config, subject: int, session: int, input_dir: str, output_dir: str):
    
    # Check if the input file exists ----------------------------------------------
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    if input_dir is None:
        input_dir = os.path.join(config['prepare']['paths']['input'], sbjname, sesname, "raw")
    input_file = os.path.join(input_dir, "fmapph.nii")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"fmapph.nii not found in {input_dir}")

    # Reorient the files to standard space ----------------------------------------
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