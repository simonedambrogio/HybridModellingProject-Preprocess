from fsl.wrappers import bet
from preprocessing.utils import get_dir_name
from preprocessing.prepare.dontsb.reorient2standard import _reorient2standard
import os

def prepare_boldwb(config, subject: int, session: int, input_dir: str = None, output_dir: str = None):
    out = _reorient2standard(config, subject, session, "boldwb", input_dir=input_dir, output_dir=output_dir)
    
    print("\033[93mStart BETting expanded_func...\033[0m")
    output_dir, output_name = get_dir_name(out)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    os.chdir(output_dir)
    bet(output_name, output_name + '_brain', f=0.015)
    print("\033[92mBETting expanded_func complete\033[0m")
    