import os, shutil, yaml, re
with open("config/cluster.yaml", "r") as f: 
    config = yaml.safe_load(f)
from preprocessing.utils import _sbjname, _sesname
def delete_file(file_path):
    try:
        # Get file size before deletion
        file_size = os.path.getsize(file_path)
        
        os.remove(file_path)
        # Force sync to ensure filesystem updates
        os.system('sync')
        
        print(f"File removed successfully (freed approximately {file_size / (1024*1024*1024):.2f} GB)")
    except FileNotFoundError:
        print("The file does not exist")
    except PermissionError:
        print("You do not have permission to delete this file")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def delete_directory(file_path):
    
    try:
        shutil.rmtree(file_path)
        print("Directory removed successfully")
    except FileNotFoundError:
        print("The directory does not exist")
    except PermissionError:
        print("You do not have permission to delete this directory")
    except Exception as e:
        print(f"An error occurred: {e}")

def make_directory(path):
    
    try:
        os.makedirs(path, exist_ok=True)
        print("Directory created successfully")
    except FileNotFoundError:
        print("The directory does not exist")
    except PermissionError:
        print("You do not have permission to delete this directory")
    except Exception as e:
        print(f"An error occurred: {e}")
        
def open_firefox(path):
    os.system(f'firefox {path} &')

# delete all files in a directory that finish with .e... or .o... (e.g. .e822892)
def delete_log_files(path):
    # Pattern matches: filename ending with .e or .o followed by digits
    pattern = r'\.(e|o)\d+$'
    
    deleted_count = 0
    for file in os.listdir(path):
        if re.search(pattern, file):
            try:
                os.remove(os.path.join(path, file))
                deleted_count += 1
            except Exception as e:
                print(f"Failed to delete {file}: {e}")
    
    print(f"Deleted {deleted_count} log files")

# Example usage
for sbj in range(13, 21):
    for run in [1,2,3,4]:
        
        sbjname, sesname = _sbjname(sbj), _sesname(run)
        path2session = os.path.join(config["preprocess"]["paths"]["output"], sbjname, sesname)
                
        delete_directory(
            os.path.join(
                path2session, 
                "logs"
            )
        )