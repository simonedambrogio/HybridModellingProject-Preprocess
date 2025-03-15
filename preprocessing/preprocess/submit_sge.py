import os
from preprocessing.utils import _sbjname, _sesname
from preprocessing.sge import SGE
from preprocessing.preprocess.dontsb import modify_fsf

# def preprocess_submit_sge(config: dict, subject: int, session: int, fsf_name: str, feat_name: str, useSpecificMask: bool = True, input_dir: str = None, output_dir: str = None, type = "sge"):
    
#     assert type in ["sge", "fsl_sub"], "Type must be either 'sge' or 'fsl_sub'"
    
#     sbjname = _sbjname(subject)
#     sesname = _sesname(session)

#     job = SGE(
#         job_name=f"preprocess_{sbjname}_{sesname}",
#         runtime="10:00:00",
#         memory="40G",
#         logdir=os.path.join(config["preprocess"]["paths"]["output"], sbjname, sesname, "logs"),
#         conda_env="fsl_sub",
#         fsl_dir=config["paths"]["FSLDIR"],
#         type=type
#     )
    
#     print(str(useSpecificMask))
#     job.submit_python_script(
#         script_path="preprocessing.preprocess.dontsb.run_preprocess",
#         args = {
#             "subject": subject,
#             "session": session,
#             "config_dir": config["paths"]["config_dir"],
#             "fsf_name": fsf_name,
#             "feat_name": feat_name,
#             "useSpecificMask": str(useSpecificMask),
#             "input_dir": input_dir,
#             "output_dir": output_dir
#         }
#     )


def preprocess_submit_sge(config: dict, subject: int, session: int, fsf_name: str, feat_name: str, useSpecificMask: bool = True, input_dir: str = None, output_dir: str = None, type = "sge"):
    
    assert type in ["sge", "fsl_sub"], "Type must be either 'sge' or 'fsl_sub'"
    
    _, fsf_dir = modify_fsf(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir)
    
    sbjname = _sbjname(subject)
    sesname = _sesname(session)

    job = SGE(
        job_name=f"preprocess_{sbjname}_{sesname}",
        memory="18G",
        logdir=os.path.join(config["preprocess"]["paths"]["output"], sbjname, sesname, "logs"),
        conda_env="fsl_sub",
        fsl_dir=config["paths"]["FSLDIR"],
        type=type
    )
    
    print(str(useSpecificMask))
    job.submit(command=f"feat {fsf_dir}", type=type, create_script=False)
