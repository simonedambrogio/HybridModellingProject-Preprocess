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
        parser.add_argument("--fsf_name", type=str, required=False, default="design.fsf")
        parser.add_argument("--feat_name", type=str, required=False, default="out")
        parser.add_argument("--input_dir", type=str, required=False, default=None)
        parser.add_argument("--output_dir", type=str, required=False, default=None)
        parser.add_argument("--useSpecificMask", type=bool, required=False, default=True)
        parser.add_argument("--make_design_only", action="store_true", help="If True, only the design will be made, but the feat will not be run")
        parser.add_argument("--submit", action="store_true", help="If True, the feat will be submitted to the cluster")
        args = parser.parse_args()
        
        sessions = [1,2,3,4] if args.session is None else [args.session]
        
        if args.make_design_only:
            if args.submit:
                print("Cannot submit to cluster when making design only")
                exit()
            args.submit = False

        for session in sessions:
            # Don't unwarp for sessions 3 and 4 of subject 14
            unwarping = 0 if session in [3,4] and args.subject == 14 else 1
            
            # Preprocess the data
            preprocess(
                config=config, 
                subject=args.subject, 
                session=session, 
                fsf_name=args.fsf_name, 
                feat_name=args.feat_name, 
                useSpecificMask=args.useSpecificMask, 
                input_dir=args.input_dir,
                output_dir=args.output_dir, 
                submit=args.submit, 
                make_design_only=args.make_design_only, 
                unwarping=unwarping,
                **config["preprocess"]["design"])
