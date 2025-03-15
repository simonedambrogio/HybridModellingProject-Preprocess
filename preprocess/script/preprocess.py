from fsl.wrappers import feat
import argparse

def preprocess(fsf_dir: str):    
    # Run FEAT
    feat(fsf_dir)
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--fsf_dir", type=str, required=True)
    args = parser.parse_args()
    preprocess(args.fsf_dir)
