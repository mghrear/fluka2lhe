# fluka2lhe
This repo uses fluka as a generator for photonuclear interactions. It provides input cards and user routines to simulate and dump photonuclear interactions including phi to K+ K- and phi to K long K short. It provides a wrapper for running fluka on a cluster. It provides scripts for processing fluka userdump files into feather and LHE files.

# Prerequisites
1. Register for a fluka account here https://fluka.cern/download/registration
2. Install fluka following the instructions here https://fluka.cern/documentation/installation
3. Install the neutron data library following instructions here https://fluka.cern/download/neutron-data-libraries

# Running fluka2lhe
## Step1: Fluka input card
Create a fluka input card and put it in the input_cards directory. The examples already provided can be used as a template.

## Step2: Routine for Fluka user-defined dump
Create an mgdraw.f routine and put it in the mgdraw_scripts directory. The examples already provided can be used as a template.

## Step3: Running Fluka
Modify top portion of either run-fluka.sh or sbatch-fluka.sh, as described in the comments. Source the .sh files to either run fluka or submit slurm jobs to run fluka. 

## Step4: fluka2feather.py
Edit fluka_sim_dir and feather_name in fluka2feather.py and run it to convert the fluka files into a pandas dataframe which is saved in feather format.

## Step5: feather2lhe.ipynb
feather2lhe.ipynb is an exploratory jupyter notebook for looking data in the the feather file. The notebook also demonstrates how the feather file can be processed into and LHE file.
