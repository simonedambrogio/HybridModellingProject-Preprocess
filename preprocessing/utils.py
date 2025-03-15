import os

def _sbjname(sbj: int):
    return f"S{str(sbj).zfill(2)}"

def _sesname(ses: int):
    return f"R{str(ses).zfill(2)}"

def get_fsf_dir(subject: int, session: int, template_dir: str):

    if (subject==14) and (session in [3,4]):
        fsfName = 'preprocess_S14_R34.fsf'
    else:
        fsfName = 'preprocess.fsf'

    return os.path.join(template_dir, fsfName), fsfName

def get_dir_name(file_path: str):
    dir = os.path.dirname(file_path)
    
    name = os.path.basename(file_path)
    name = name.split('.')[0]
    
    return dir, name

def get_name_ext(file_path: str):
    name = os.path.basename(file_path)
    name = name.split('.')[0]
    ext = name.split('.')[-1]
    return name, ext