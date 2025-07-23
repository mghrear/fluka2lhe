#!/bin/bash

# Define the base path for the Fluka commands here
FLUKA_PATH="/home/groups/laurenat/majd/fluka4-5.0"

# Define the target directory here
TARGET_DIR="/home/groups/laurenat/majd/fluka2lhe/test4"

# Define the files to copy
mgdraw_script="mgdraw_phiKK.f"
input_card="phiKK_4550.inp"

# Define the range for random seeds
SEED_START=1	# Starting seed number
SEED_END=10	# Ending seed number

# Define the number of statistically independent runs per seed
Num_runs=1  # Set the desired number of runs here

# Make target directory if it doesn't already exist
if [ ! -d "$TARGET_DIR" ]; then
    mkdir $TARGET_DIR
fi

# Copy the files to the target directory
echo "Copying '$mgdraw_script' to '$TARGET_DIR'..." 
cp "mgdraw_scripts/$mgdraw_script" "$TARGET_DIR"

# Compile mgdraw.f routine
echo "Running $FLUKA_PATH/bin/fff $mgdraw_script"
$FLUKA_PATH/bin/fff $TARGET_DIR/$mgdraw_script

# Create executable
echo "Running $FLUKA_PATH/bin/lfluka -o mgdraw_phiKK.o"
$FLUKA_PATH/bin/lfluka -o $TARGET_DIR/phiKK_exe $TARGET_DIR/mgdraw_phiKK.o

# Generate a list of random seeds from SEED_START to SEED_END
for ((seed=SEED_START; seed<=SEED_END; seed++)); do
	
	# Create a directory for each seed, copy the fluka input card there and update the random seed
	SEED_DIR="$TARGET_DIR/$seed"
	mkdir -p "$SEED_DIR"  # Create the directory, -p ensures no error if it exists
	cp "input_cards/$input_card" "$SEED_DIR"
	sed -i "34s/.*/RANDOMIZ         1.0        $seed/" "$SEED_DIR/$input_card"

	# Print the created seed directory
	echo "Created directory: $SEED_DIR"

	# cd to seed directior
	cd $SEED_DIR

	echo "Running $FLUKA_PATH/bin/rfluka -e $TARGET_DIR/phiKK_exe $TARGET_DIR/phiKK_4550.inp -M $Num_runs"
	$FLUKA_PATH/bin/rfluka -e $TARGET_DIR/phiKK_exe $SEED_DIR/phiKK_4550.inp -M "$Num_runs"

done

echo "All commands executed successfully."

