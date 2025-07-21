# fluka2lhe
Converts fluka userdump output into an lhe file

## Modifying the fluka input card
Will update later

## Modifying the mgdraw.f routine
Will update later

## Running fluka in command line
1. Install fluka following the instructions here https://fluka.cern/documentation/installation
2. Compile the provided mgdraw_phiKK.f routine with the command: /path/to/fluka/bin/fff mgdraw_phiKK.f
3. Create an executable with the command: /path/to/fluka/bin/lfluka -m fluka -o phiKK_exe  mgdraw_phiKK.o
4. Run fluka with the command: /path/to/fluka/bin/rfluka -e phiKK_exe phiKK_4500.inp -M [number of statistically independent runs]
 
