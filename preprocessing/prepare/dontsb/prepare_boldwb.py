from fsl.wrappers import bet
from preprocessing.utils import get_dir_name
from preprocessing.prepare.dontsb.reorient2standard import _reorient2standard
import os
from preprocessing.utils import _sbjname, _sesname

def prepare_boldwb(config, subject: int, session: int, input_dir: str = None, output_dir: str = None):
    
    # Check if the input file exists ----------------------------------------------
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    if input_dir is None:
        input_dir = os.path.join(config['prepare']['paths']['input'], sbjname, sesname, "raw")
    input_file = os.path.join(input_dir, "boldwb.nii")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"boldwb.nii not found in {input_dir}")
    
    # Reorient the files to standard space ----------------------------------------
    out = _reorient2standard(config, subject, session, "boldwb", input_dir=input_dir, output_dir=output_dir)
    
    print("\033[93mStart BETting expanded_func...\033[0m")
    output_dir, output_name = get_dir_name(out)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    os.chdir(output_dir)
    bet(output_name, output_name + '_brain', f=0.015)
    print("\033[92mBETting expanded_func complete\033[0m")
    