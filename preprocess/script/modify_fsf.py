import yaml, os, sys, argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils import _sbjname, _sesname, get_fsf_dir
from string import Template
import nibabel as nib
import numpy as np

def modify_fsf(
        config: dict,
        subject: int, 
        session: int, 
        useSpecificMask: bool = True,
        fsf_name: str = "design.fsf",
        feat_name: str = "out",
        **custom_subs
    ):
    
    sbjname = _sbjname(subject)
    sesname = _sesname(session)

    prepare_dir = os.path.join(config['prepare']['paths']['output'], sbjname, sesname)
    preprocess_dir = os.path.join(config['preprocess']['paths']['output'], sbjname, sesname)
    func_dir = os.path.join(prepare_dir, "func_biascorr.nii.gz")
    template_dir, fsfname = get_fsf_dir(subject, session, config['preprocess']['paths']['template'])
 
    with open(template_dir, 'r') as f:
        template = Template(f.read())
    
    
    fmap_rads_dir = os.path.join(prepare_dir, "fmap_rads.nii.gz")
    fmap_mag_dir = os.path.join(prepare_dir, "fmap_mag_brain.nii.gz")
    whole_func_dir = os.path.join(prepare_dir, "expanded_func_brain.nii.gz")
    struct_brain_dir = os.path.join(prepare_dir, "synthstrip_biascorr_brain.nii.gz")
    alternative_mask_dir = os.path.join(config['paths']["data"], "fsl", "data", str(subject), str(session), "first-level", "funcmask.nii.gz")
    
    # Prepare substitution dictionary
    img = nib.load(func_dir)
    subs = {
        'outputdir': os.path.join(preprocess_dir, feat_name),
        'tr': get_tr(img),
        'te': 27,
        'volumes': get_volumes(img),
        'smooth': 2.0,
        'reginitial_highres_dof': 12, # Degrees of Freedom for registration to initial highres
        'standard': config['preprocess']['paths']['standard'],
        'regstandard_dof': 12, # Degrees of Freedom for registration to standard space
        'totalVoxels': get_total_voxels(img),
        'prepared_func': func_dir,
        'fmap_rads': fmap_rads_dir,
        'fmap_mag': fmap_mag_dir,
        'whole_func': whole_func_dir,
        'structural': struct_brain_dir,
        'alternative_mask': alternative_mask_dir if useSpecificMask else "",
    }
    
    # Update with any custom substitutions
    subs.update(custom_subs)
    
    fsf_content = template.substitute(subs)
    fsf_dir = save_fsf(preprocess_dir, fsf_content, fsf_name)
    return fsf_content, fsf_dir

def get_volumes(img: nib.Nifti1Image):
    return img.header['dim'][4]

def get_tr(img: nib.Nifti1Image):
    return img.header['pixdim'][4]

def get_total_voxels(img: nib.Nifti1Image):
    """
    Calculate the total number of voxels in a NIfTI image.
    
    Parameters:
    -----------
    img : nib.Nifti1Image
        The NIfTI image object
        
    Returns:
    --------
    int
        Total number of voxels
    """
    # Get dimensions from header
    dims = img.header.get("dim")[1:5]
    
    # Use numpy's prod function with dtype=np.int64 to avoid overflow
    total_voxels = np.prod(dims, dtype=np.int64)
    
    return int(total_voxels)

def save_fsf(output_dir: str, fsf_content: str, name: str = "design"):
    
    if not name.endswith(".fsf"):
        name = name + ".fsf"

    print(name)
    # Write output FSF file
    output_fsf = os.path.join(output_dir, name)   
    os.makedirs(output_dir, exist_ok=True)
    with open(output_fsf, 'w') as f:
        f.write(fsf_content)
    
    print(output_fsf)
    return output_fsf

if __name__ == "__main__":
    
    import yaml
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--useSpecificMask", type=bool, default=True)
    parser.add_argument("--fsf_name", type=str, default="design.fsf")
    parser.add_argument("--feat_name", type=str, default="out")
    
    # Add a more flexible way to specify substitution parameters
    parser.add_argument("--subs", nargs="+", help="Substitution parameters in format key=value, e.g. --subs smooth=2.0 reginitial_highres_dof=12 regstandard_dof=12 te=27")
    
    args = parser.parse_args()
    
    # Extract custom substitutions from args
    custom_subs = {}
    
    # Process any substitution parameters
    if args.subs:
        for sub in args.subs:
            if '=' in sub:
                key, value = sub.split('=', 1)
                # Try to convert value to appropriate type
                try:
                    # Try as int
                    custom_subs[key] = int(value)
                except ValueError:
                    try:
                        # Try as float
                        custom_subs[key] = float(value)
                    except ValueError:
                        # Keep as string
                        custom_subs[key] = value
    
    modify_fsf(config, args.subject, args.session, args.useSpecificMask, 
               args.fsf_name, args.feat_name, **custom_subs)