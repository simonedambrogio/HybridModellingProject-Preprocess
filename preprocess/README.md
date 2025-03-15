# Preprocess Module

The preprocess module runs the FSL FEAT preprocessing pipeline on prepared fMRI data. It handles the configuration of FEAT parameters, execution of the preprocessing steps, and supports submission to computing clusters.

## Overview

The preprocess module takes the prepared fMRI data from the prepare module and runs it through FSL's FEAT (FMRI Expert Analysis Tool) preprocessing pipeline. This includes:

1. **FSF File Modification**: Customizes the FSL FEAT design file (FSF) with subject-specific parameters
2. **FEAT Preprocessing**: Runs the FSL FEAT preprocessing pipeline with the modified FSF file
3. **Cluster Submission**: Optionally submits preprocessing jobs to computing clusters

## Running the Preprocess Module

The main entry point is `preprocess.py`, which can be run as follows:

```bash
# Run for a specific subject and session
python preprocess.py --subject 1 --session 1

# Run for a specific subject, all sessions
python preprocess.py --subject 1

# Submit to cluster (SLURM by default)
python preprocess.py --subject 1 --submit_to slurm

# Submit to SGE cluster
python preprocess.py --subject 1 --submit_to sge

# Run with custom parameters
python preprocess.py --subject 1 --session 1 --fsf_name custom_design.fsf --feat_name custom_output
```

### Command Line Arguments

- `--subject`: Subject ID (required)
- `--session`: Session number (optional, runs all sessions if not specified)
- `--submit_to`: Cluster type to submit to (choices: "slurm", "sge"). Specifying this option automatically enables job submission.
- `--type`: Type of submission command (choices: "sge", "fsl_sub", default: "sge")
- `--fsf_name`: Name of the FSF template file (default: "design.fsf")
- `--feat_name`: Name of the output FEAT directory (default: "out")
- `--input_dir`: Custom input directory (optional)
- `--output_dir`: Custom output directory (optional)
- `--useSpecificMask`: Whether to use subject-specific brain mask (default: True)

## Preprocess Steps in Detail

### 1. FSF File Modification

**Purpose**: Customizes the FSL FEAT design file (FSF) with subject-specific parameters.

**Steps**:
1. Loads the template FSF file
2. Replaces template variables with subject-specific values:
   - Input functional data path
   - Output directory
   - Number of volumes
   - TR (repetition time)
   - Brain mask path (if using subject-specific mask)
   - Other preprocessing parameters
3. Saves the modified FSF file to the output directory

**Implementation**:
```python
def modify_fsf(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir, **custom_subs):
    # Load template FSF file
    template_dir, fsfname = get_fsf_dir(subject, session, config['preprocess']['paths']['template'])
    with open(template_dir, 'r') as f:
        template = Template(f.read())
    
    # Set up substitution dictionary with subject-specific values
    subs = {
        'FEAT_DIR': os.path.join(output_dir, feat_name),
        'FUNC_DATA': func_dir,
        'TOTAL_VOLUMES': get_volumes(nib.load(func_dir)),
        'TR_VALUE': get_tr(nib.load(func_dir)),
        # Additional substitutions...
    }
    
    # Apply substitutions to template
    fsf_content = template.safe_substitute(subs)
    
    # Save modified FSF file
    fsf_dir = save_fsf(output_dir, fsf_content, name=fsf_name.split('.')[0])
    return fsf_content, fsf_dir
```

### 2. FEAT Preprocessing

**Purpose**: Runs the FSL FEAT preprocessing pipeline with the modified FSF file.

**Steps**:
1. Calls the FSL FEAT command with the modified FSF file
2. FEAT performs preprocessing steps as specified in the FSF file, which typically include:
   - Motion correction
   - Slice timing correction
   - Spatial smoothing
   - Intensity normalization
   - High-pass temporal filtering
   - Registration to standard space

**Implementation**:
```python
def preprocess(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir):
    # Modify FSF file
    _, fsf_dir = modify_fsf(config, subject, session, fsf_name, feat_name, useSpecificMask, input_dir, output_dir)
    
    # Run FEAT
    feat(fsf_dir)
```

## Cluster Submission

The preprocess module supports submitting jobs to computing clusters:

- **SLURM**: For SLURM-based clusters
- **SGE**: For Sun Grid Engine-based clusters

When the `--submit_to` parameter is specified, the module will automatically create and submit appropriate job scripts to the specified cluster system.

### Submission Types

The module supports two types of submission commands:

- **SGE**: Uses custom SGE submission scripts
- **FSL_SUB**: Uses FSL's built-in submission command

## Configuration

The preprocessing pipeline uses configuration parameters from `config/cluster.yaml`, including:

- Paths to input and output directories
- Paths to template FSF files
- Cluster submission parameters

## Integration with Prepare Module

The preprocess module is designed to work with the output of the prepare module. By default, it looks for prepared data in the prepare module's output directory and saves preprocessed data to its own output directory.

You can override these defaults by specifying custom input and output directories using the `--input_dir` and `--output_dir` command line arguments. 