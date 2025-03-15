# Prepare Module

The prepare module is responsible for preparing raw fMRI data for preprocessing. It performs several critical steps to ensure data is properly formatted and ready for the FSL FEAT preprocessing pipeline.

## Overview

The prepare module consists of several key components that work together to prepare different types of fMRI data:

1. **bold4d**: Prepares 4D functional MRI data
2. **struct**: Prepares structural (anatomical) MRI data
3. **boldwb**: Prepares whole-brain functional MRI data
4. **fmap**: Prepares field map data for distortion correction

## Running the Prepare Module

The main entry point is `prepare.py`, which can be run as follows:

```bash
# Run for a specific subject and session
python prepare.py --subject 1 --session 1

# Run for a specific subject, all sessions
python prepare.py --subject 1

# Submit to cluster
python prepare.py --subject 1 --submit_to slurm

# Submit to SGE cluster
python prepare.py --subject 1 --submit_to sge
```

### Command Line Arguments

- `--subject`: Subject ID (required)
- `--session`: Session number (optional, runs all sessions if not specified)
- `--submit_to`: Cluster type to submit to (choices: "slurm", "sge"). Specifying this option automatically enables job submission.

## Prepare Steps in Detail

### 1. bold4d Preparation

**Purpose**: Prepares 4D functional MRI data for preprocessing.

**Steps**:
1. Reorients the 4D functional data to standard space using FSL's `fslreorient2std`
2. Performs bias field correction to remove intensity non-uniformities

**Implementation**:
```python
def prepare_bold4d(config, subject, session, input_dir=None, output_dir=None):
    # Reorient to standard space
    _reorient2standard(config, subject, session, "bold4d", input_dir, output_dir)
    
    # Bias field correction
    _biascorrect(config, subject, session, "func", input_dir, output_dir)
```

### 2. Structural Data Preparation

**Purpose**: Prepares structural (anatomical) MRI data for preprocessing.

**Steps**:
1. Reorients the structural data to standard space
2. Performs brain extraction using SynthStrip
3. Copies the brain-extracted, bias-corrected image to the output directory
4. Cleans up intermediate files

**Implementation**:
```python
def prepare_struct(config, subject, session, input_dir, output_dir):
    # Reorient to standard space
    anat_input = _reorient2standard(config, subject, session, "mprage", input_dir, output_dir)
    
    # Brain extraction with SynthStrip
    anat_output = os.path.join(output_dir, "struct_brain")
    _anat_synthstrip(anat_input, anat_output)
    
    # Copy final output and clean up
    anat_output_dir = os.path.join(output_dir, "struct_brain.anat")
    file_from = os.path.join(anat_output_dir, "synthstrip_biascorr_brain.nii.gz")
    file_to = os.path.join(output_dir, "synthstrip_biascorr_brain.nii.gz")
    shutil.copy(file_from, file_to)
    shutil.rmtree(anat_output_dir)
```

### 3. Whole-Brain Functional Data Preparation

**Purpose**: Prepares whole-brain functional MRI data for preprocessing.

**Steps**:
1. Reorients the whole-brain functional data to standard space
2. Performs brain extraction using FSL's BET with a fractional intensity threshold of 0.015

**Implementation**:
```python
def prepare_boldwb(config, subject, session, input_dir=None, output_dir=None):
    # Reorient to standard space
    out = _reorient2standard(config, subject, session, "boldwb", input_dir, output_dir)
    
    # Brain extraction with BET
    output_dir, output_name = get_dir_name(out)
    os.chdir(output_dir)
    bet(output_name, output_name + '_brain', f=0.015)
```

### 4. Field Map Preparation

**Purpose**: Prepares field map data for distortion correction in the preprocessing pipeline.

**Steps**:
1. Reorients both phase and magnitude field map images to standard space
2. Performs brain extraction on the magnitude image
3. Erodes the brain mask to avoid edge effects
4. Creates a field map in radians/second using `fsl_prepare_fieldmap`

**Implementation**:
```python
def prepare_fmap(config, subject, session, input_dir, output_dir):
    # Reorient phase and magnitude images to standard space
    out_fmapph = _reorient2standard(config, subject, session, "fmapph", input_dir, output_dir)
    out_fmapmg = _reorient2standard(config, subject, session, "fmapmg", input_dir, output_dir)
    
    output_dir, fmapph_name = get_dir_name(out_fmapph)
    _, fmapmg_name = get_dir_name(out_fmapmg)
    
    os.chdir(output_dir)
    
    # Brain extraction
    bet(fmapmg_name, fmapmg_name + '_brain')
    bet(fmapph_name, fmapph_name + '_brain', f=0.015)
    
    # Erode brain mask
    fslmaths(fmapmg_name + '_brain').ero().ero().run(fmapmg_name + '_brain_ero')
    
    # Create field map in radians/second
    fsl_prepare_fieldmap(fmapph_name + '.nii.gz', fmapmg_name + '_brain_ero.nii.gz', 'fmap_rads', 1.02)
```

## Common Utilities

### Reorientation to Standard Space

**Purpose**: Ensures all images are in the same orientation as the standard MNI template.

**Implementation**: Uses FSL's `fslreorient2std` to reorient images.

### Bias Field Correction

**Purpose**: Removes intensity non-uniformities from MRI images.

**Implementation**: Uses FSL's `fast` for bias field correction.

### Brain Extraction

**Purpose**: Removes non-brain tissue from MRI images.

**Implementation**: 
- For structural data: Uses SynthStrip for accurate brain extraction
- For functional data: Uses FSL's BET with appropriate fractional intensity thresholds

## Cluster Submission

The prepare module supports submitting jobs to computing clusters:

- **SLURM**: For SLURM-based clusters
- **SGE**: For Sun Grid Engine-based clusters

When the `--submit_to` parameter is specified, the module will automatically create and submit appropriate job scripts to the specified cluster system.

## Session-Specific Processing

Note that structural, whole-brain functional, and field map preparation are only performed for sessions 1 and 3, as shown in the main function:

```python
def main(config, subject, session, submit, submit_to):
    prepare.bold4d(config, subject, session, submit=submit, submit_to=submit_to)
    if session in [1,3]:
        prepare.struct(config, subject, session, submit=submit, submit_to=submit_to)
        prepare.boldwb(config, subject, session, submit=submit, submit_to=submit_to)
        prepare.fmap(config, subject, session, submit=submit, submit_to=submit_to)
```

This is because these data types are typically only acquired in specific sessions of the experiment. 