import numpy as np
import pandas as pd 
import Fluka_dump_tools as fdt
import os
from pathlib import Path

# Path of directory with fluka simulations to convert
fluka_sim_dir = "/home/groups/laurenat/majd/fluka_sims/3740_MeV/"

# Name of final feather file
feather_name = "phiKK_3740_MeV.ftr"

####################################################################################



# List all subdirectories, there should be a subdirectory for each seed
#subdirs = [str(subdir) for subdir in Path(fluka_sim_dir).iterdir() if subdir.is_dir()]
subdirs = ["/home/groups/laurenat/majd/fluka_sims/3740_MeV/1","/home/groups/laurenat/majd/fluka_sims/3740_MeV/2"]

df = pd.DataFrame()

#Loop through subdirectories
for path in subdirs:
	# Get list of paths the files with .90 extension
	matching_files = fdt.find_files_with_extension(path, '.90')

	for file_path in matching_files:
		
		print("readng: ", file_path)		

		# Convert file to a pandas dataframe
		df_i = fdt.Fluka2Pandas(file_path)

		# Append to main dataframe
		df = pd.concat([df, df_i], ignore_index=True)

df.to_feather(fluka_sim_dir+feather_name)
