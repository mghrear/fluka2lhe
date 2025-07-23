#!/bin/bash

# Define the base path for the Fluka commands here
FLUKA_PATH="/home/groups/laurenat/majd/fluka4-5.0"

# Specifiy durectory where simulations are output
TARGET_DIR="/home/groups/laurenat/majd/fluka2lhe/test4"

# Select mgdraw scripr and fluka inputcard to use
mgdraw_script="mgdraw_phiKK.f"
input_card="phiKK_4550.inp"

# Define the range for random seeds
SEED_START=1	# Starting seed number
SEED_END=10	# Ending seed number

# Define the number of statistically independent runs per seed
Num_runs=1  # Set the desired number of runs here

#fluka2lhe filepath
f2l_path="/home/groups/laurenat/majd/fluka2lhe"

# Get current directory
CURRENT_DIR=$(pwd)

# Define new mgdraw files based on the existing file
mgdraw_o="${mgdraw_script%.f}.o"       # Remove the .f extension for the object file.
mgdraw_exe="${mgdraw_script%.f}_exe"   # Append _exe to the base name for the executable.

# Make target directory if it doesn't already exist
if [ ! -d "$TARGET_DIR" ]; then
    mkdir $TARGET_DIR
fi

# Copy the files to the target directory
echo "Copying '$mgdraw_script' to '$TARGET_DIR'..." 
cp "$f2l_path/mgdraw_scripts/$mgdraw_script" "$TARGET_DIR"

# Compile mgdraw.f routine
echo "Running $FLUKA_PATH/bin/fff $mgdraw_script"
$FLUKA_PATH/bin/fff $TARGET_DIR/$mgdraw_script

# Create executable
echo "Running $FLUKA_PATH/bin/lfluka -o $mgdraw_o"
$FLUKA_PATH/bin/lfluka -o $TARGET_DIR/$mgdraw_exe $TARGET_DIR/$mgdraw_o

# Generate a list of random seeds from SEED_START to SEED_END
for ((seed=SEED_START; seed<=SEED_END; seed++)); do
	
	# Create a directory for each seed, copy the fluka input card there and update the random seed
	SEED_DIR="$TARGET_DIR/$seed"
	mkdir -p "$SEED_DIR"  # Create the directory, -p ensures no error if it exists
	cp "$f2l_path/input_cards/$input_card" "$SEED_DIR"
	sed -i "34s/.*/RANDOMIZ         1.0    $seed./" "$SEED_DIR/$input_card"

	# Print the created seed directory
	echo "Created directory: $SEED_DIR"

	# cd to seed directior
	cd $SEED_DIR

	echo "Running $FLUKA_PATH/bin/rfluka -e $TARGET_DIR/$mgdraw_exe $TARGET_DIR/$input_card -M $Num_runs"
	$FLUKA_PATH/bin/rfluka -e $TARGET_DIR/$mgdraw_exe $SEED_DIR/$input_card -M "$Num_runs"

done

# Return to current directory
cd $CURRENT_DIR 
echo "All commands executed successfully."

