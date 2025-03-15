import sys, os, yaml
with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
        
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from preprocessing.preprocess.preprocess import preprocess

if __name__ == "__main__":
        import argparse, yaml
        with open("config/cluster.yaml", "r") as f: 
            config = yaml.safe_load(f)
            
        parser = argparse.ArgumentParser()
        parser.add_argument("--subject", type=int, required=True)
        parser.add_argument("--session", type=int, required=False, default=None)
        parser.add_argument("--submit_to", type=str, required=False, default="slurm", choices=["slurm", "sge"])
        parser.add_argument("--type", type=str, required=False, default="sge", choices=["sge", "fsl_sub"])
        parser.add_argument("--fsf_name", type=str, required=False, default="design.fsf")
        parser.add_argument("--feat_name", type=str, required=False, default="out")
        parser.add_argument("--input_dir", type=str, required=False, default=None)
        parser.add_argument("--output_dir", type=str, required=False, default=None)
        parser.add_argument("--useSpecificMask", type=bool, required=False, default=True)
        args = parser.parse_args()
        
        sessions = [1,2,3,4] if args.session is None else [args.session]
        submit = False if args.submit_to == None else True

        for session in sessions:
            preprocess(config, args.subject, session, args.fsf_name, args.feat_name, args.useSpecificMask, args.input_dir, args.output_dir, submit, args.submit_to, args.type)
