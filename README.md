# fluka2lhe
Converts fluka userdump output into an lhe file

# Prerequisites
1. Register for a fluka account here https://fluka.cern/download/registration
2. Install fluka following the instructions here https://fluka.cern/documentation/installation
3. Install the neutron data library following instructions here https://fluka.cern/download/neutron-data-libraries

# Running fluka2lhe
## Step1: Modifying the fluka input card
Will update later

## Step2: Modifying the mgdraw.f routine
Will update later

## Step3: Modifying the fluka2lhe-run.sh
Will update later


1. Compile the provided mgdraw_phiKK.f routine with the command: /path/to/fluka/bin/fff mgdraw_phiKK.f
2. Create an executable with the command: /path/to/fluka/bin/lfluka -m fluka -o phiKK_exe  mgdraw_phiKK.o
3. Run fluka with the command: /path/to/fluka/bin/rfluka -e phiKK_exe phiKK_4500.inp -M [number of statistically independent runs]
 
