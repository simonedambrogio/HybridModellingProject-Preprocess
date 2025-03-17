from preprocessing.prepare.dontsb.reorient2standard import _reorient2standard
from preprocessing.prepare.dontsb.biascorrect import _biascorrect
from preprocessing.utils import _sbjname, _sesname
import os

def prepare_bold4d(config, subject: int, session: int, input_dir: str = None, output_dir: str = None):
    
    # Check if the input file exists ----------------------------------------------
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    if input_dir is None:
        input_dir = os.path.join(config['prepare']['paths']['input'], sbjname, sesname, "raw")
    input_file = os.path.join(input_dir, "bold4d.nii")
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"bold4d.nii not found in {input_dir}")
    
    # Reorient2Standard
    print("Reorienting bold4d to standard...")
    _reorient2standard(config, subject, session, "bold4d", input_dir=input_dir, output_dir=output_dir)
    
    # Bias Correction
    print("Bias correcting bold4d...")
    input_dir = output_dir
    _biascorrect(config, subject, session, "func", input_dir, output_dir)
