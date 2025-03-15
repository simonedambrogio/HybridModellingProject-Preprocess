# Preprocessing Pipeline

A pipeline for preprocessing human fMRI data with FSL.

## Components

### 1. Prepare

Prepares raw fMRI data for preprocessing by performing initial data organization and preprocessing steps.

```bash
# Run for a specific subject and session
python prepare/prepare.py --subject 1 --session 1

# Run for a specific subject, all sessions
python prepare/prepare.py --subject 1

# Submit to cluster
python prepare/prepare.py --subject 1 --submit True --submit_to slurm
```

### 2. Preprocess

Runs the FSL FEAT preprocessing pipeline on the prepared data.

```bash
# Run for a specific subject and session
python preprocess/preprocess.py --subject 1 --session 1

# Run with custom parameters
python preprocess/preprocess.py --subject 1 --session 1 --fsf_name design.fsf --feat_name out --useSpecificMask True

# Submit to cluster
python preprocess/preprocess.py --subject 1 --session 1 --submit_to slurm --type sge
```

### 3. Check Status

Checks the status of preprocessing, verifies required files, and manages intermediate files.

```bash
# Check status for a specific subject and session (print-only mode)
python check-status.py --subject 1 --session 1

# Check status for all subjects and sessions
python check-status.py

# Perform actions (cleanup files, create symbolic links)
python check-status.py --subject 1 --session 1 --action
```

In print-only mode (default), suggestions for actions are highlighted in yellow. Use the `--action` flag to actually perform these operations.

## Workflow

1. **Prepare**: Organize and prepare raw data
2. **Check Status**: Verify all required files exist
3. **Preprocess**: Run the FSL FEAT preprocessing
4. **Check Status**: Verify preprocessing completed and clean up intermediate files

## Configuration

All settings are stored in `config/cluster.yaml`. 