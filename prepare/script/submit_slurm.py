import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
from utils import _sbjname, _sesname
from simple_slurm import Slurm

def reorient2standard_submit_slurm(config, subject: int, session: int, inputname: str, input_dir: str, output_dir: str, outputname: str = None):
    
    if outputname is None:
        outputname = config["raw2prepared"][inputname]
    
    if os.path.exists(os.path.join(output_dir, outputname)):
        return None
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    reorient2standard_script = os.path.join(script_dir, "reorient2standard.py")
    
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    # Create a Slurm object with the job parameters
    slurm = Slurm(
        job_name=f"reorient2std_{sbjname}_{sesname}",
        partition="short",
        time="0:10:00",
        output=os.path.join(output_dir, "logs", f"reorient2std_{sbjname}_{sesname}.out"),
        error=os.path.join(output_dir, "logs", f"reorient2std_{sbjname}_{sesname}.err")
    )
    
    # Make sure logs directory exists
    os.makedirs(os.path.join(output_dir, "logs"), exist_ok=True)
    
    # Create the command to run
    cmd = (
        f"python {reorient2standard_script} "
        f"--subject {subject} "
        f"--session {session} "
        f"--inputname {inputname} "
        f"--outputname {outputname} "
        f"--input_dir {input_dir} "
        f"--output_dir {output_dir}"
    )
    
    # Run the sbatch command
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"Reorient2standard job ID: {job_id}")
    
def biascorrect_submit_slurm(config, subject: int, session: int, input_dir: str, output_dir: str, job_id: int = None):
    
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    biascorrect_script = os.path.join(script_dir, "biascorrect.py")

    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    slurm = Slurm(
        job_name=f"biascorrect_{sbjname}_{sesname}",
        partition="short",
        time="00:20:00",
        output=os.path.join(output_dir, "logs", f"biascorrect_{sbjname}_{sesname}.out"),
        error=os.path.join(output_dir, "logs", f"biascorrect_{sbjname}_{sesname}.err")
    )
    if job_id is not None:
        slurm.add_dependency(f"afterok:{job_id}")
    
    # Run the command
    cmd = (
        f"python {biascorrect_script} "
        f"--subject {subject} "
        f"--session {session} "
        f"--input_dir {input_dir} "
        f"--output_dir {output_dir}"
    )
    
    # Run the sbatch command
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"Bias correct job ID: {job_id}")
    
def fsl_anat_submit_slurm(subject: int, session: int, inputname: str, outputname: str, input_dir: str, output_dir: str, t: str):
    
    # Check if the output image already exists
    if os.path.exists(os.path.join(output_dir, outputname)):
        return None
    
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    slurm = Slurm(
        job_name=f"fsl_anat_{sbjname}_{sesname}",
        partition="short",
        time="00:40:00",
        output=os.path.join(output_dir, "logs", f"fsl_anat_{sbjname}_{sesname}.out"),
        error=os.path.join(output_dir, "logs", f"fsl_anat_{sbjname}_{sesname}.err")
    )
    
    input_image = os.path.join(input_dir, inputname)
    output_image = os.path.join(output_dir, outputname)
    
    cmd = (
        f"fsl_anat -i {input_image} -o {output_image} -t {t}"
    )
    
    # Run the sbatch command
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"FSL ANAT job ID: {job_id}")

def synthstrip_submit_slurm(subject: int, session: int, input_image: str, output_image: str, brain_mask: str, output_dir: str, job_id: int = None):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    # Create a Slurm object with the job parameters
    slurm = Slurm(
        job_name=f"synthstrip_{sbjname}_{sesname}",
        partition="short",
        time="00:05:00",
        output=os.path.join(output_dir, "logs", f"synthstrip_{sbjname}_{sesname}.out"),
        error=os.path.join(output_dir, "logs", f"synthstrip_{sbjname}_{sesname}.err")
    )
    if job_id is not None:
        slurm.add_dependency(f"afterok:{job_id}")

    # Create the command to run
    cmd = (
        f"/vols/Scratch/flange/bin/synthstrip-singularity "
        f"-i {input_image} "
        f"-o {output_image} "
        f"-m {brain_mask} "
        f"--no-csf"
    )
    
    # Run the sbatch command
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"Synthstrip job ID: {job_id}")

def anat_synthstrip_submit_slurm(config: dict, subject: int, session: int, anat_input: str, anat_output: str, output_dir: str, job_id: int = None):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    anat_synthstrip_script = os.path.join(script_dir, "anat_synthstrip.py")
    
    slurm = Slurm(
        job_name=f"anat_synthstrip_{sbjname}_{sesname}",
        partition="short",
        time="00:40:00",
        output=os.path.join(output_dir, "logs", f"anat_synthstrip_{sbjname}_{sesname}.out"),
        error=os.path.join(output_dir, "logs", f"anat_synthstrip_{sbjname}_{sesname}.err")
    )
    if job_id is not None:
        slurm.add_dependency(f"afterok:{job_id}")
    
    # Run the command
    cmd = (
        f"python {anat_synthstrip_script} "
        f"--anat_input {anat_input} "
        f"--anat_output {anat_output} "
    )
    
    # Run the sbatch command
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"Anat Synthstrip job ID: {job_id}")

def prepare_struct_submit_slurm(config: dict, subject: int, session: int, input_dir: str, output_dir: str):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    prepare_struct_script = os.path.join(script_dir, "prepare_struct.py")
    
    slurm = Slurm(
        job_name=f"prepare_struct_{sbjname}_{sesname}",
        partition="short",
        time="01:30:00",
        output=os.path.join(output_dir, "logs", f"prepare_struct_{sbjname}_{sesname}.out"),
        error=os.path.join(output_dir, "logs", f"prepare_struct_{sbjname}_{sesname}.err")
    )
    
    # Run the command
    cmd = (
        f"python {prepare_struct_script} "
        f"--subject {subject} "
        f"--session {session} "
        f"--input_dir {input_dir} "
        f"--output_dir {output_dir}"
    )
    
    # Run the sbatch command
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"Prepare Struct job ID: {job_id}")

def prepare_bold4d_submit_slurm(config: dict, subject: int, session: int, input_dir: str, output_dir: str):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    prepare_brain4d_script = os.path.join(script_dir, "prepare_brain4d.py")
    
    slurm = Slurm(
        job_name=f"prepare_brain4d_{sbjname}_{sesname}",
        partition="short",
        time="00:20:00",
        output=os.path.join(output_dir, "logs", f"prepare_brain4d_{sbjname}_{sesname}.out"),
        error=os.path.join(output_dir, "logs", f"prepare_brain4d_{sbjname}_{sesname}.err")
    )
    
    # Run the command
    cmd = (
        f"python {prepare_brain4d_script} "
        f"--subject {subject} "
        f"--session {session} "
        f"--input_dir {input_dir} "
        f"--output_dir {output_dir}"
    )
    
    # Run the sbatch command
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"Prepare Bold4d job ID: {job_id}")

def prepare_boldwb_submit_slurm(config: dict, subject: int, session: int, input_dir: str, output_dir: str):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    prepare_boldwb_script = os.path.join(script_dir, "prepare_boldwb.py")
    
    slurm = Slurm(
        job_name=f"prepare_boldwb_{sbjname}_{sesname}",
        partition="short",
        time="00:02:00",
        output=os.path.join(output_dir, "logs", f"prepare_boldwb_{sbjname}_{sesname}.out"),
        error=os.path.join(output_dir, "logs", f"prepare_boldwb_{sbjname}_{sesname}.err")
    )
    
    # Run the command
    cmd = (
        f"python {prepare_boldwb_script} "
        f"--subject {subject} "
        f"--session {session} "
        f"--input_dir {input_dir} "
        f"--output_dir {output_dir}"
    )
    
    # Run the sbatch command
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"Prepare BoldWB job ID: {job_id}")

def prepare_fmap_submit_slurm(config: dict, subject: int, session: int, input_dir: str, output_dir: str):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    prepare_fmap_script = os.path.join(script_dir, "prepare_fmap.py")
    
    slurm = Slurm(
        job_name=f"prepare_fmap_{sbjname}_{sesname}",
        partition="short",
        time="00:02:00",
        output=os.path.join(output_dir, "logs", f"prepare_fmap_{sbjname}_{sesname}.out"),
        error=os.path.join(output_dir, "logs", f"prepare_fmap_{sbjname}_{sesname}.err")
    )
    
    # Run the command
    cmd = (
        f"python {prepare_fmap_script} "
        f"--subject {subject} "
        f"--session {session} "
        f"--input_dir {input_dir} "
        f"--output_dir {output_dir}"
    )
    
    # Run the sbatch command
    print(f"Submitting job: {cmd}")
    job_id = slurm.sbatch(cmd)
    print(f"Prepare Fmap job ID: {job_id}")

if __name__ == "__main__":
    import yaml
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", type=str)
    parser.add_argument("--subject", type=int)
    parser.add_argument("--session", type=int)
    parser.add_argument("--inputname", type=str)
    parser.add_argument("--input_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    parser.add_argument("--outputname", type=str, default=None)
    args = parser.parse_args()
    
    if args.script == "reorient2standard":
        reorient2standard_submit_slurm(config, args.subject, args.session, args.inputname, args.input_dir, args.output_dir)
    elif args.script == "biascorrect":
        job_id = None
        biascorrect_submit_slurm(config, args.subject, args.session, args.input_dir, args.output_dir, job_id)
    