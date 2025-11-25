import numpy as np
import pandas as pd 
import Fluka_dump_tools as fdt
import os
from pathlib import Path

# Path of directory with fluka simulations to convert
fluka_sim_dir = "/home/groups/laurenat/majd/fluka_sims/KLKS/4550_MeV"

# Name of final feather file
feather_name = "phiKLKS_4550_MeV"

####################################################################################

# List all subdirectories, there should be a subdirectory for each seed
subdirs = [str(subdir) for subdir in Path(fluka_sim_dir).iterdir() if subdir.is_dir()]

# List to store dataframes
dataframes = []


# fort 90 file counter
n_files = 0 

#Loop through subdirectories correspondng to different seeds
for path in subdirs:

	# For each subdirectory create a list of paths to .90 files
	matching_files = fdt.find_files_with_extension(path, '.90')

	for file_path in matching_files:

		try:
			print("reading: ", file_path, " ...")		

			# Convert file to a pandas dataframe
			df_i = fdt.Fluka2Pandas(file_path)

			# Append to the list of dataframes
			dataframes.append(df_i)

			# Increment file counter
			n_files += 1

		except Exception as e:
			print(f"Error reading {file_path}: {e}")

# Concatenate all dataframes and save
df = pd.concat(dataframes, ignore_index=True)
df.to_feather(fluka_sim_dir+feather_name+"_"+str(n_files)+"_files.ftr")

