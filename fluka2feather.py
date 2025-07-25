import numpy as np
import pandas as pd 
import Fluka_dump_tools as fdt
import os
from pathlib import Path

# Path of directory with fluka simulations to convert
fluka_sim_dir = "/home/groups/laurenat/majd/fluka_sims/4550_MeV/"

# Name of final feather file
feather_name = "phiKK_4550_MeV"

####################################################################################

# List all subdirectories, there should be a subdirectory for each seed
subdirs = [str(subdir) for subdir in Path(fluka_sim_dir).iterdir() if subdir.is_dir()]

# Dataframe to store data
df = pd.DataFrame()

# fort 90 file counter
n_files = 0 

#Loop through subdirectories correspondng to different seeds
for path in subdirs:

	# For each subdirectory create a list of paths to .90 files
	matching_files = fdt.find_files_with_extension(path, '.90')

	for file_path in matching_files:
		
		print("reading: ", file_path, " ...")		

		# Convert file to a pandas dataframe
		df_i = fdt.Fluka2Pandas(file_path)

		# Append to main dataframe
		df = pd.concat([df, df_i], ignore_index=True)

		# Increment file counter
		n_files += 1

df.to_feather(fluka_sim_dir+feather_name+"_"+str(n_files)+"_files.ftr")
