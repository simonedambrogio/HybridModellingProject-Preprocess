import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import preprocessing.prepare as prepare
import yaml
from preprocessing.utils import _sbjname, _sesname

with open("config/cluster.yaml", "r") as f: 
    config = yaml.safe_load(f)

for subject in range(1, 21):
    for session in range(1, 5):
        fileout = os.path.join(config['prepare']['paths']['output'], _sbjname(subject), _sesname(session), "func_biascorr.nii.gz")
        if os.path.exists(fileout):
            print(f"\033[93mOutput file {fileout} exists, skipping . . .\033[0m")
        else:
            print(f"\033[91mOutput file {fileout} does not exist, running biascorrect . . .\033[0m")
            # prepare.bold4d(config, subject, session, submit=True, submit_to="sge")
