import os

from preprocessing.utils import _sbjname, _sesname
from fsl.wrappers import fast
from fsl.wrappers import fslmaths

def _biascorrect(config, subject: int, session: int, inputname: str, input_dir: str, output_dir: str):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)

    # Get directories
    if input_dir is None:
        input_dir = os.path.join(config['paths']['prepare'], "output", sbjname, sesname)
    if output_dir is None:
        output_dir = os.path.join(config['paths']['prepare'], "output", sbjname, sesname)

    if inputname.endswith(".nii.gz"):
        input_nameext = inputname
        input_name = inputname.split(".nii.gz")[0]
    else:
        input_nameext = inputname + ".nii.gz"
        input_name = inputname
        
    func = os.path.join(input_dir, input_nameext)
    bias_field = os.path.join(output_dir, input_name + "_field")
    func_biascorr = os.path.join(output_dir, input_name + "_biascorr.nii.gz")

    print("Run fast directly using the wrapper...")
    fast(func, type=2, out=bias_field, b=True)

    print("Run fslmaths...")
    fslmaths(func).div(bias_field + '_bias').run(func_biascorr)

    print("Remove non-biascorrected func and temporary files")
    files_to_remove = [
        func,
        bias_field + '_bias' + '.nii.gz',
        os.path.join(output_dir, "func_field_mixeltype.nii.gz"),
        os.path.join(output_dir, "func_field_pve_0.nii.gz"),
        os.path.join(output_dir, "func_field_pve_1.nii.gz"),
        os.path.join(output_dir, "func_field_pve_2.nii.gz"),
        os.path.join(output_dir, "func_field_pveseg.nii.gz"),
        os.path.join(output_dir, "func_field_restore.nii.gz"),
        os.path.join(output_dir, "func_field_seg.nii.gz")
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)

