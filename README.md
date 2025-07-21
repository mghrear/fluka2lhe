# fluka2lhe
Converts fluka userdump output into an lhe file

# Requirements
1. Install fluka following the instructions here https://fluka.cern/documentation/installation
2. Install the neutron data library following instructions here https://fluka.cern/download/neutron-data-libraries

## Modifying the fluka input card
Will update later

## Modifying the mgdraw.f routine
Will update later

## Running fluka in command line
1. Compile the provided mgdraw_phiKK.f routine with the command: /path/to/fluka/bin/fff mgdraw_phiKK.f
2. Create an executable with the command: /path/to/fluka/bin/lfluka -m fluka -o phiKK_exe  mgdraw_phiKK.o
3. Run fluka with the command: /path/to/fluka/bin/rfluka -e phiKK_exe phiKK_4500.inp -M [number of statistically independent runs]
 
