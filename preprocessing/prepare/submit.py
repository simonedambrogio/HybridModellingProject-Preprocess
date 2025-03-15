import os
import argparse
# Use relative imports
from .submit_slurm import *
from .submit_sge import *

def reorient2standard_submit(config, subject: int, session: int, inputname: str, input_dir: str, output_dir: str, outputname: str = None, submit: str = "slurm"):
    assert submit in ["slurm", "sge"], f"Submit method {submit} not supported"
    if submit == "slurm":
        reorient2standard_submit_slurm(config, subject, session, inputname, input_dir, output_dir, outputname)
    elif submit == "sge":
        reorient2standard_submit_sge(config, subject, session, inputname, input_dir, output_dir, outputname)
    else:
        raise ValueError(f"Submit method {submit} not supported")

def biascorrect_submit(config, subject: int, session: int, inputname: str, input_dir: str, output_dir: str, job_id: int = None, submit: str = "slurm"):
    assert submit in ["slurm", "sge"], f"Submit method {submit} not supported"
    if submit == "slurm":
        biascorrect_submit_slurm(config, subject, session, inputname, input_dir, output_dir, job_id)
    elif submit == "sge":
        biascorrect_submit_sge(config, subject, session, inputname, input_dir, output_dir, job_id)
    else:
        raise ValueError(f"Submit method {submit} not supported")

def prepare_struct_submit(config: dict, subject: int, session: int, input_dir: str, output_dir: str, submit: str = "slurm"):
    assert submit in ["slurm", "sge"], f"Submit method {submit} not supported"
    if submit == "slurm":
        prepare_struct_submit_slurm(config, subject, session, input_dir, output_dir)
    elif submit == "sge":
        prepare_struct_submit_sge(config, subject, session, input_dir, output_dir)
    else:
        raise ValueError(f"Submit method {submit} not supported")

def prepare_bold4d_submit(config: dict, subject: int, session: int, input_dir: str, output_dir: str, submit: str = "slurm"):
    assert submit in ["slurm", "sge"], f"Submit method {submit} not supported"
    if submit == "slurm":
        prepare_bold4d_submit_slurm(config, subject, session, input_dir, output_dir)
    elif submit == "sge":
        prepare_bold4d_submit_sge(config, subject, session, input_dir, output_dir)
    else:
        raise ValueError(f"Submit method {submit} not supported")
    
def prepare_boldwb_submit(config: dict, subject: int, session: int, input_dir: str, output_dir: str, submit: str = "slurm"):
    assert submit in ["slurm", "sge"], f"Submit method {submit} not supported"
    if submit == "slurm":
        prepare_boldwb_submit_slurm(config, subject, session, input_dir, output_dir)
    elif submit == "sge":
        prepare_boldwb_submit_sge(config, subject, session, input_dir, output_dir)
    else:
        raise ValueError(f"Submit method {submit} not supported")

def prepare_fmap_submit(config: dict, subject: int, session: int, input_dir: str, output_dir: str, submit: str = "slurm"):
    assert submit in ["slurm", "sge"], f"Submit method {submit} not supported"
    if submit == "slurm":
        prepare_fmap_submit_slurm(config, subject, session, input_dir, output_dir)
    elif submit == "sge":
        prepare_fmap_submit_sge(config, subject, session, input_dir, output_dir)
    else:
        raise ValueError(f"Submit method {submit} not supported")

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
    parser.add_argument("--submit", type=str, default="slurm")
    args = parser.parse_args()
    
    if args.script == "reorient2standard":
        reorient2standard_submit(config, args.subject, args.session, args.inputname, args.input_dir, args.output_dir, args.outputname, args.submit)
    elif args.script == "biascorrect":
        job_id = None
        biascorrect_submit(config, args.subject, args.session, args.input_dir, args.output_dir, job_id, args.submit)
    elif args.script == "prepare_struct":
        prepare_struct_submit(config, args.subject, args.session, args.input_dir, args.output_dir, args.submit)
    elif args.script == "prepare_bold4d":
        prepare_bold4d_submit(config, args.subject, args.session, args.input_dir, args.output_dir, args.submit)
    elif args.script == "prepare_boldwb":
        prepare_boldwb_submit(config, args.subject, args.session, args.input_dir, args.output_dir, args.submit)
    elif args.script == "prepare_fmap":
        prepare_fmap_submit(config, args.subject, args.session, args.input_dir, args.output_dir, args.submit)
    else:
        raise ValueError(f"Script {args.script} not supported")
