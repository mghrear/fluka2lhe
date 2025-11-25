#!/bin/bash
#SBATCH --job-name=f2f  # Job name
#SBATCH --output=f2f.out  # Output file name (includes job ID)
#SBATCH --error=f2f.err   # Error file name (includes job ID)
#SBATCH --time=24:00:00             # Time limit (HH:MM:SS)
#SBATCH --partition=normal          # Partition to use (e.g., normal, gpu)
#SBATCH --ntasks=1                  # Number of tasks
#SBATCH --cpus-per-task=1           # Number of CPUs per task
#SBATCH --mem=20G                    # Memory per node
#SBATCH --mail-type=ALL             # Send email for all states
#SBATCH --mail-user=mghrear@stanford.edu # Replace with your email

# Setup env
source ~/.bashrc
conda activate pandas_env

# Execute your commands
python fluka2feather.py 
