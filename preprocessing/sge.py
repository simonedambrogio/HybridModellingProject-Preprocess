import os
import subprocess
from typing import List, Dict, Optional, Union, Any


class SGE:
    """
    A class to handle SGE (Sun Grid Engine) job submissions.
    """
    
    def __init__(self, 
                 job_name: str,
                 runtime: Optional[str] = None,
                 queue: Optional[str] = None,
                 memory: Optional[str] = None,
                 logdir: str = "logs",
                 conda_env: Optional[str] = None,
                 fsl_dir: Optional[str] = None,
                 working_dir: Optional[str] = None,
                 env_vars: Optional[Dict[str, str]] = None,
                 type: str = "sge"):
        """
        Initialize an SGE job submission object.
        
        Args:
            job_name: Name of the job
            runtime: Runtime limit in format "HH:MM:SS"
            queue: SGE queue to submit to
            memory: Memory requirement (e.g. "4G")
            logdir: Directory for output and error logs
            conda_env: Conda environment to activate
            fsl_dir: Path to FSL installation
            working_dir: Working directory for the job (defaults to current directory)
            env_vars: Additional environment variables to set
            type: Type of submission system ("sge" or "fsl_sub")
        """
        self.job_name = job_name
        self.runtime = runtime
        self.queue = queue
        self.memory = memory
        self.logdir = logdir
        self.conda_env = conda_env
        self.fsl_dir = fsl_dir
        self.working_dir = working_dir or os.getcwd()
        self.env_vars = env_vars or {}
        self.type = type
        # Create output directory if it doesn't exist
        os.makedirs(self.logdir, exist_ok=True)
    
    def create_script(self, command: str, script_path: Optional[str] = None) -> str:
        """
        Create a shell script for the job.
        
        Args:
            command: The command to run
            script_path: Path to save the script (default: logdir/job_name.sh)
            
        Returns:
            Path to the created script
        """
        if script_path is None:
            script_path = os.path.join(self.logdir, f"{self.job_name}.sh")
            
        with open(script_path, "w") as f:
            f.write("#!/bin/bash\n\n")
            
            # Set working directory
            f.write(f"cd {self.working_dir}\n\n")
            
            # Set up FSL environment if specified
            if self.fsl_dir:
                f.write("# Set up FSL environment\n")
                f.write(f"FSLDIR={self.fsl_dir}\n")
                f.write("source ${FSLDIR}/etc/fslconf/fsl.sh\n")
                f.write("export FSLDIR PATH\n\n")
            
            # Set additional environment variables
            if self.env_vars:
                f.write("# Set additional environment variables\n")
                for key, value in self.env_vars.items():
                    f.write(f"export {key}={value}\n")
                f.write("\n")
            
            # Add the command - no need to modify it here since we'll use the full Python path
            f.write("# Run the command\n")
            f.write(f"{command}\n")
        
        # Make the script executable
        os.chmod(script_path, 0o755)
        
        return script_path
    
    def submit(self, command: str, script_path: Optional[str] = None, type: str = "sge", create_script: bool = True) -> Optional[str]:
        """
        Submit a job to the cluster.
        
        Args:
            command: The command to run
            script_path: Path to save the script (default: logdir/job_name.sh)
            type: Type of submission system ("sge" or "fsl_sub")
            
        Returns:
            Job ID if successful, None otherwise
        """
        # Create the script
        script_path = self.create_script(command, script_path) if create_script else command
        
        # Build submission command
        if type == "sge":
            # SGE qsub command
            qsub_cmd = ["qsub", "-N", self.job_name]
            
            # Add resource requirements
            resource_args = []
            if self.runtime:
                resource_args.append(f"h_rt={self.runtime}")
            if self.memory:
                resource_args.append(f"mem_free={self.memory}")  
            if resource_args:
                qsub_cmd.extend(["-l", ",".join(resource_args)])
            
            # Add queue if specified
            if self.queue:
                qsub_cmd.extend(["-q", self.queue])
            
            # Add output and error file paths
            output_file = os.path.join(self.logdir, f"{self.job_name}.out")
            error_file = os.path.join(self.logdir, f"{self.job_name}.err")
            qsub_cmd.extend([
                "-o", output_file,
                "-e", error_file
            ])
            
            # Add the script path
            qsub_cmd.append(script_path)
            
        elif type == "fsl_sub":
            # fsl_sub command
            qsub_cmd = ["fsl_sub", "-N", self.job_name]
            
            # Add resource requirements
            if self.runtime:
                # Convert HH:MM:SS to minutes for -T option
                if ":" in self.runtime:
                    parts = self.runtime.split(":")
                    if len(parts) == 3:  # HH:MM:SS
                        hours, minutes, _ = map(int, parts)
                        total_minutes = hours * 60 + minutes
                    elif len(parts) == 2:  # HH:MM
                        hours, minutes = map(int, parts)
                        total_minutes = hours * 60 + minutes
                    else:
                        total_minutes = int(self.runtime)
                else:
                    total_minutes = int(self.runtime)
                qsub_cmd.extend(["-T", str(total_minutes)])
            
            if self.memory:
                # Convert memory string to GB for -R option
                if self.memory.endswith("G"):
                    gb = int(self.memory[:-1])
                elif self.memory.endswith("M"):
                    gb = int(self.memory[:-1]) // 1024
                elif self.memory.endswith("K"):
                    gb = int(self.memory[:-1]) // (1024 * 1024)
                else:
                    gb = int(self.memory)
                qsub_cmd.extend(["-R", str(gb)])
            
            # Add queue if specified
            if self.queue:
                qsub_cmd.extend(["-q", self.queue])
            
            # Add log directory
            if self.logdir:
                qsub_cmd.extend(["-l", self.logdir])
            
            # Add any additional environment variables to export
            if self.env_vars:
                for key, value in self.env_vars.items():
                    qsub_cmd.extend(["--export", f"{key}={value}"])
            
            # Add the script path (for fsl_sub, the command is the last argument)
            qsub_cmd.append(script_path)
        
        else:
            raise ValueError(f"Unknown submission type: {type}")
        
        # Save the submission command to the output file
        output_file = os.path.join(self.logdir, f"{self.job_name}.out")
        submission_info = f"Submitting job: {' '.join(qsub_cmd)}\n"
        submission_info += f"Working directory: {self.working_dir}\n"
        submission_info += f"Command: {command}\n\n"
        
        # Create the output file and write the submission info
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(submission_info)
        
        # Submit the job
        process = subprocess.Popen(qsub_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            job_id = stdout.decode().strip()
            print(f"\033[92mJob submitted with ID: {job_id}\033[0m")
            
            # Append the job ID to the output file
            with open(output_file, 'a') as f:
                f.write(f"Job ID: {job_id}\n")
                f.write("=" * 50 + "\n\n")
            
            return job_id
        else:
            print(f"\033[91mError submitting job: {stderr.decode()}\033[0m")
            
            # Write the error to the output file
            with open(output_file, 'a') as f:
                f.write(f"Error submitting job: {stderr.decode()}\n")
            
            return None
    
    def submit_python_script(self, 
                            script_path: str, 
                            args: Optional[Dict[str, Any]] = None,
                            python_path: Optional[str] = None) -> Optional[str]:
        """
        Submit a Python script as a job.
        
        Args:
            script_path: Path to the Python script
            args: Dictionary of arguments to pass to the script
            python_path: Path to the Python interpreter (default: uses conda_env if specified)
            
        Returns:
            Job ID if successful, None otherwise
        """
        # Determine the Python path
        if python_path is None:
            if self.conda_env:
                # Use the full path to the Python executable in the conda environment
                python_path = f"/home/fs0/jdf650/scratch/miniconda3/envs/{self.conda_env}/bin/python"
            else:
                # Use the default Python
                python_path = "python"
        
        # Build the command
        if script_path.startswith("preprocessing.") or "." in script_path and "/" not in script_path:
            # It's a module path, use -m flag
            cmd = f"{python_path} -m {script_path}"
        else:
            # It's a file path
            cmd = f"{python_path} {script_path}"
        
        # Add arguments
        if args:
            for key, value in args.items():
                if value is None:
                    continue
                elif isinstance(value, bool) and value:
                    cmd += f" --{key}"
                else:
                    cmd += f" --{key} {value}"
        
        # Submit the job
        return self.submit(cmd, type=self.type) 