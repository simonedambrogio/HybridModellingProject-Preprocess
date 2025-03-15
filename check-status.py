#!/usr/bin/env python
"""
Check Input Files for Preprocessing

This script verifies that all required input files for preprocessing exist and
helps manage intermediate files to save disk space.

Key features:
1. Checks if all required input files exist in the prepare folder
2. Identifies unnecessary intermediate files that can be safely removed
3. Creates symbolic links for missing files when possible (for sessions 2 and 4)
4. Provides a safe "print-only" mode (default) that shows what would be done
5. Offers an action mode (--action flag) to actually perform the operations

When run without the --action flag, the script only prints information about
what would be done (files to remove, links to create). When run with the --action flag,
it actually performs these operations - removing unnecessary files and creating
symbolic links for missing files.
"""

import os
from preprocessing.utils import _sbjname, _sesname
    
def _cleanup(config, subject: int, session: int, feat_name: str, print_only: bool):
    """
    Identify and optionally remove unnecessary intermediate files.
    a
    This function performs two cleanup operations:
    1. Removes files not in the 'files2keep' list from the prepare folder
    2. Removes func_biascorr.nii.gz if filtered_func_data.nii.gz exists (to save space)
    
    Args:
        config (dict): Configuration dictionary containing paths and file lists
        subject (int): Subject number
        session (int): Session number
        feat_name (str): Name of the FEAT output directory
        print_only (bool): If True, only print what would be removed without deleting
                          If False, actually delete the files
    
    Returns:
        None
    """
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    
    # Remove files that are not in the files2keep list -------------------------------------
    files2keep = config['prepare']['files2keep']
    files = os.listdir(os.path.join(config["prepare"]["paths"]["output"], sbjname, sesname))
    removes_files = []
    for file in files:
        if file not in files2keep:
            removes_files.append(file)
            if not print_only:
                os.remove(os.path.join(config["prepare"]["paths"]["output"], sbjname, sesname, file))
    
    print(f"\t\033[92m✅ {"Removing" if not print_only else "You need to remove"} {len(removes_files)} file{'s' if len(removes_files) != 1 else ''} from the prepare folder\033[0m. {"\033[93mset --action to remove them.\033[0m" if print_only and len(removes_files) > 0 else ""}\033[0m")
    if len(removes_files) > 0:
        for (i, file) in enumerate(removes_files):
            print(f"\t\t\033[91m{i+1}. {file}\033[0m")

    # Remove func_biascorr.nii.gz if out.feat/filtered_func_data.nii.gz exists ------------
    bias_corr_file = os.path.join(config["prepare"]["paths"]["output"], sbjname, sesname, "func_biascorr.nii.gz")
    if filtered_func_exists(config, subject, session, feat_name) and os.path.exists(bias_corr_file):
        if not print_only:
            os.remove(bias_corr_file)
        print(f"\t\033[92m✅ {"Removing" if not print_only else "You can remove"} func_biascorr.nii.gz from the prepare folder to save space.\033[0m {"\033[93mset --action to remove it.\033[0m" if print_only else ""}\033[0m")
    
def get_fileout(config: dict, input: str, subject: int, session: int):
    """
    Get the full path to an input file in the prepare output directory.
    
    Args:
        config (dict): Configuration dictionary containing paths
        input (str): Input file name
        subject (int): Subject number
        session (int): Session number
        
    Returns:
        str: Full path to the input file
    """
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    return os.path.join(config['prepare']['paths']['output'], sbjname, sesname, input)

def filtered_func_exists(config: dict, subject: int, session: int, feat_name: str):
    """
    Check if the filtered functional data exists in the preprocessing output.
    
    This is used to determine if func_biascorr.nii.gz can be safely removed.
    
    Args:
        config (dict): Configuration dictionary containing paths
        subject (int): Subject number
        session (int): Session number
        feat_name (str): Name of the FEAT output directory
        
    Returns:
        bool: True if filtered_func_data.nii.gz exists, False otherwise
    """
    sbjname = _sbjname(subject)
    sesname = _sesname(session)
    return os.path.exists(os.path.join(config['preprocess']['paths']['output'], sbjname, sesname, feat_name, "filtered_func_data.nii.gz"))

def check_status(config: dict, subject: int, session: int, feat_name: str, action: bool = False):
    """
    Check if all required input files exist and manage intermediate files.
    
    This function:
    1. Checks if all required preprocessing input files exist
    2. For missing files in sessions 2 or 4, checks if they exist in the previous session
       and creates symbolic links if possible (when action=True)
    3. Identifies and optionally removes unnecessary intermediate files
    
    Args:
        config (dict): Configuration dictionary containing paths and file lists
        subject (int): Subject number
        session (int): Session number
        feat_name (str): Name of the FEAT output directory
        action (bool, optional): If True, actually perform operations (remove files, create links).
                                If False (default), only print what would be done.
    
    Returns:
        None
    """
    print(f"\nSubject: {subject}, Session: {session}")
    
    # If filtered_func_data exists, we don't need func_biascorr.nii.gz anymore
    if filtered_func_exists(config, subject, session, feat_name):
        preprocess_inputs = [item for item in config['preprocess']['inputs'] if item != "func_biascorr.nii.gz"]
    else:
        preprocess_inputs = config['preprocess']['inputs']
    
    # Check if all the inputs required for preprocessing exist in the prepare folder ---------
    if all(os.path.exists(get_fileout(config, input, subject, session)) for input in preprocess_inputs):
        if filtered_func_exists(config, subject, session, feat_name):
            print(f"\t\033[92m✅ Preprocess succesfully completed.\033[0m")
        else:
            print(f"\t\033[92m✅ All the inputs required for preprocessing exist in the prepare folder.\033[0m")    
            print(f"\t\t\033[93mYou can start preprocessing!\033[0m")    
    else:
        print(f"\t\033[91m❌ Some of the inputs required for preprocessing do not exist in the prepare folder.\033[0m")
        for input in config['preprocess']['inputs']:
            fileout = get_fileout(config, input, subject, session)
            if not os.path.exists(fileout):
                filename = os.path.basename(fileout)
                # does it exist in the session-1 folder?
                if session in [2, 4]:
                    fileout_sm1 = get_fileout(config, input, subject, session-1)
                    file_exists_in_sessionm1 = os.path.exists(fileout_sm1)
                    if action and file_exists_in_sessionm1:
                        os.symlink(fileout_sm1, fileout)
                        print(f"\t\033[92m✅ Symbolic link created for {filename}.\033[0m")
                    else:
                        print(f"\t\033[91m❌ File {filename} does not exist.\033[0m{f"\033[93m Use --action to fix it.\033[0m" if file_exists_in_sessionm1 else f"\033[93m Create it for session {session-1} first."}\033[0m")
                else:
                    print(f"\t\033[91m❌ File {filename} does not exist.\033[0m")          
                                                                            
    # Run cleanup function (print_only=True means it will only show what would be deleted)
    _cleanup(config, subject, session, feat_name, print_only=not action)

if __name__ == "__main__":
    import argparse, yaml
    
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description="""
        Check if all required input files for preprocessing exist and manage intermediate files.
        
        By default, this script runs in 'print-only' mode, which shows what files could be
        removed without actually deleting anything. This is safe to run at any time.
        
        To actually remove the identified files, use the --action flag.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--subject", type=int, help="Subject number (if omitted, checks all subjects 1-20)")
    parser.add_argument("--session", type=int, help="Session number (if omitted, checks all sessions 1-4)")
    parser.add_argument("--feat_name", type=str, default="out.feat", help="Name of the FEAT output directory (default: out.feat)")
    parser.add_argument("--action", action="store_true", help="Actually remove unnecessary files (without this flag, only prints what would be removed)")
    args = parser.parse_args()
    
    # Load configuration
    with open("config/cluster.yaml", "r") as f: 
        config = yaml.safe_load(f)
    
    # Determine which subjects and sessions to process
    subjects = range(1, 21) if args.subject is None else [args.subject]
    sessions = range(1, 5) if args.session is None else [args.session]
    
    # Print mode information
    if args.action:
        print("\033[93mRunning in Action mode: Unnecessary files will be DELETED and symbolic links will be created\033[0m")
    else:
        print("\n\033[92m===============================================================\033[0m")
        print("\033[92mRunning in PRINT-ONLY mode: No files will be deleted or created\033[0m")
        print("\033[92m- Items that need attention will be highlighted in \033[93myellow\033[92m")
        print("- Use --action to perform all suggested operations (delete files, create symbolic links)\033[0m")
        print("\033[92m===============================================================\033[0m")
    
    # Process each subject and session
    for subject in subjects:
        for session in sessions:
            check_status(config, subject, session, args.feat_name, args.action)
