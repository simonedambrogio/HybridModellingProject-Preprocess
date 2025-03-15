import os, yaml, subprocess
from preprocessing.utils import _sbjname, _sesname

def initial_highres2example_func(config, subject: int, session: int, dof: int):
    sbjname, sesname = _sbjname(subject), _sesname(session)
    input_dir = os.path.join(
        config["paths"]["info-sampling-task-data"], sbjname, sesname, 
        "preprocess", "output-1mm.feat", "reg")

    output_dir = os.path.join(
        config["preprocess"]["paths"]["output"], sbjname, sesname, 
        f"out_{dof}")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run flirt from pythin
    cmd = [
        "flirt", 
        "-in", os.path.join(input_dir, "example_func.nii.gz"), 
        "-ref", os.path.join(input_dir, "initial_highres.nii.gz"), 
        "-out", os.path.join(output_dir, f"example_func2initial_highres_{dof}dof.nii.gz"), 
        "-omat", os.path.join(output_dir, f"example_func2initial_highres_{dof}dof.mat"), 
        "-cost", "corratio", 
        "-dof", str(dof), 
        "-searchrx", "-90", "90", "-searchry", "-90", "90", 
        "-searchrz", "-90", "90", "-interp", "trilinear"
    ]
    
    if dof == 3:
        cmd.append("-schedule") 
        cmd.append("/home/fs0/jdf650/scratch/FSL/etc/flirtsch/sch3Dtrans_3dof")
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Running registration...")
    stdout, stderr = process.communicate()
    print(f"Registration complete.")
    

if __name__ == "__main__":
    import argparse, yaml
   
    parser = argparse.ArgumentParser()
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--dof", type=int, required=True)
    args = parser.parse_args()

    with open("config/cluster.yaml", "r") as f:
        config = yaml.safe_load(f)
    initial_highres2example_func(config, args.subject, args.session, args.dof)








