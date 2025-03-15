import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import argparse
from utils import _sbjname, _sesname
from sge import SGE

def reorient2standard_submit_sge(config, subject: int, session: int, inputname: str, input_dir: str, output_dir: str, outputname: str = None):
    
    sbjname = _sbjname(subject)
    sesname = _sesname(session)

    if outputname is None:
        outputname = config["raw2prepared"][inputname]
    if output_dir is None:
        output_dir = os.path.join(config["prepare"]["paths"]["output"], sbjname, sesname)
    if input_dir is None:
        input_dir = os.path.join(config["prepare"]["paths"]["input"], sbjname, sesname, "raw")
    
    if os.path.exists(os.path.join(output_dir, outputname)):
        return None
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    reorient2standard_script = os.path.join(script_dir, "reorient2standard.py")
    
    # Make sure logs directory exists
    logs_dir = os.path.join(output_dir, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # Create SGE job
    job = SGE(
        job_name=f"reorient2std_{sbjname}_{sesname}_{inputname}",
        runtime="0:10:00",
        logdir=logs_dir,
        conda_env="fsl_sub",
        fsl_dir=config["paths"]["FSLDIR"]
    )
    
    # Submit the job
    return job.submit_python_script(
        script_path=reorient2standard_script,
        args={
            "subject": subject,
            "session": session,
            "inputname": inputname,
            "outputname": outputname,
            "input_dir": input_dir,
            "output_dir": output_dir
        }
    )

def biascorrect_submit_sge(config, subject: int, session: int, inputname: str, input_dir: str, output_dir: str, job_id: int = None):
    
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    if output_dir is None:
        output_dir = os.path.join(config["prepare"]["paths"]["output"], sbjname, sesname)
        
    script_dir = os.path.join(config['paths']['prepare'], "script")
    biascorrect_script = os.path.join(script_dir, "biascorrect.py")
    
    job = SGE(
        job_name=f"biascorrect_{sbjname}_{sesname}_{inputname}",
        runtime="0:20:00",
        logdir=os.path.join(output_dir, "logs"),
        conda_env="fsl_sub",
        fsl_dir=config["paths"]["FSLDIR"]
    )
    
    # Run the sbatch command
    job.submit_python_script(
        script_path=biascorrect_script,
        args={
            "subject": subject,
            "session": session,
            "inputname": inputname,
            "input_dir": input_dir,
            "output_dir": output_dir
        }
    )

def prepare_struct_submit_sge(config: dict, subject: int, session: int, input_dir: str, output_dir: str):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    if input_dir is None:
        input_dir = os.path.join(config["prepare"]["paths"]["input"], sbjname, sesname, "raw")
    if output_dir is None:
        output_dir = os.path.join(config["prepare"]["paths"]["output"], sbjname, sesname)
        
    script_dir = os.path.join(config['paths']['prepare'], "script")
    prepare_struct_script = os.path.join(script_dir, "prepare_struct.py")
    
    job = SGE(
        job_name=f"prepare_struct_{sbjname}_{sesname}",
        runtime="1:30:00",
        logdir=os.path.join(output_dir, "logs"),
        conda_env="fsl_sub",
        fsl_dir=config["paths"]["FSLDIR"]
    )
    
    # Run the command
    job.submit_python_script(
        script_path=prepare_struct_script,
        args={
            "subject": subject,
            "session": session,
            "input_dir": input_dir,
            "output_dir": output_dir
        }
    )
    
def prepare_bold4d_submit_sge(config: dict, subject: int, session: int, input_dir: str, output_dir: str):
    
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    if input_dir is None:
        input_dir = os.path.join(config["prepare"]["paths"]["input"], sbjname, sesname, "raw")
    if output_dir is None:
        output_dir = os.path.join(config["prepare"]["paths"]["output"], sbjname, sesname)
        
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    prepare_bold4d_script = os.path.join(script_dir, "prepare_bold4d.py")
    
    job = SGE(
        job_name=f"prepare_bold4d_{sbjname}_{sesname}",
        runtime="0:20:00",
        logdir=os.path.join(output_dir, "logs"),
        conda_env="fsl_sub",
        fsl_dir=config["paths"]["FSLDIR"]
    )
    
    # Run the command
    job.submit_python_script(
        script_path=prepare_bold4d_script,
        args={
            "subject": subject,
            "session": session,
            "input_dir": input_dir,
            "output_dir": output_dir
        }
    )

def prepare_boldwb_submit_sge(config: dict, subject: int, session: int, input_dir: str, output_dir: str):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    if input_dir is None:
        input_dir = os.path.join(config["prepare"]["paths"]["input"], sbjname, sesname, "raw")
    if output_dir is None:
        output_dir = os.path.join(config["prepare"]["paths"]["output"], sbjname, sesname)
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    prepare_boldwb_script = os.path.join(script_dir, "prepare_boldwb.py")
    
    job = SGE(
        job_name=f"prepare_boldwb_{sbjname}_{sesname}",
        runtime="0:02:00",
        logdir=os.path.join(output_dir, "logs"),
        conda_env="fsl_sub",
        fsl_dir=config["paths"]["FSLDIR"]
    )
    
    # Run the command
    job.submit_python_script(
        script_path=prepare_boldwb_script,
        args={
            "subject": subject,
            "session": session,
            "input_dir": input_dir,
            "output_dir": output_dir
        }
    )

def prepare_fmap_submit_sge(config: dict, subject: int, session: int, input_dir: str, output_dir: str):
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    if input_dir is None:
        input_dir = os.path.join(config["prepare"]["paths"]["input"], sbjname, sesname, "raw")
    if output_dir is None:
        output_dir = os.path.join(config["prepare"]["paths"]["output"], sbjname, sesname)
    
    script_dir = os.path.join(config['paths']['prepare'], "script")
    prepare_fmap_script = os.path.join(script_dir, "prepare_fmap.py")
    
    job = SGE(
        job_name=f"prepare_fmap_{sbjname}_{sesname}",
        runtime="0:02:00",
        logdir=os.path.join(output_dir, "logs"),
        conda_env="fsl_sub",
        fsl_dir=config["paths"]["FSLDIR"]
    )
    
    # Run the command
    job.submit_python_script(
        script_path=prepare_fmap_script,
        args={
            "subject": subject,
            "session": session,
            "input_dir": input_dir,
            "output_dir": output_dir
        }
    )
    

if __name__ == "__main__":
    
    import yaml
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", type=str, required=True)
    parser.add_argument("--subject", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--inputname", type=str, required=False)
    parser.add_argument("--input_dir", type=str, required=False)
    parser.add_argument("--output_dir", type=str, required=False)
    parser.add_argument("--outputname", type=str, default=None)
    args = parser.parse_args()
    
    if args.script == "reorient2standard":
        reorient2standard_submit_sge(config, args.subject, args.session, args.inputname, args.input_dir, args.output_dir, args.outputname)
    elif args.script == "biascorrect":
        biascorrect_submit_sge(config, args.subject, args.session, args.inputname, args.input_dir, args.output_dir)
    elif args.script == "prepare_struct":
        prepare_struct_submit_sge(config, args.subject, args.session, args.input_dir, args.output_dir)
    elif args.script == "prepare_bold4d":
        prepare_bold4d_submit_sge(config, args.subject, args.session, args.input_dir, args.output_dir)
    elif args.script == "prepare_boldwb":
        prepare_boldwb_submit_sge(config, args.subject, args.session, args.input_dir, args.output_dir)
    elif args.script == "prepare_fmap":
        prepare_fmap_submit_sge(config, args.subject, args.session, args.input_dir, args.output_dir)
    else:
        raise ValueError(f"Script {args.script} not found")
    