from preprocessing.prepare.dontsb.reorient2standard import _reorient2standard
from preprocessing.prepare.dontsb.biascorrect import _biascorrect

def prepare_bold4d(config, subject: int, session: int, input_dir: str = None, output_dir: str = None):
    
    # Reorient2Standard
    print("Reorienting bold4d to standard...")
    _reorient2standard(config, subject, session, "bold4d", input_dir=input_dir, output_dir=output_dir)
    
    # Bias Correction
    print("Bias correcting bold4d...")
    input_dir = output_dir
    _biascorrect(config, subject, session, "func", input_dir, output_dir)
