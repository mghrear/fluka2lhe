import numpy as np
import pandas as pd 

# Get PDG ID, Mass [GeV], and Charge from fluka particle ID
flukaIDdict = {
    1: (2212, 0.938, 1),      # (PDG ID, Mass [GeV], Charge)
    2: (-2212, 0.938, -1),
    3: (11, 0.000511, -1),
    4: (-11, 0.000511, 1),
    7: (22, 0, 0),
    8: (2112, 0.9396, 0),
    9: (-2112, 0.9396, 0),
    10: (-2112, 0.10566, 1),
    11: (-2112, 0.10566, -1),
    12: (130, 0.497611 , 0),
    13: (211, 0.13957, 1),
    14: (-211, 0.13957, -1),
    15: (321, 0.493677, 1),
    16: (-321, 0.493677, -1),
    17: (3122, 1.1156, 0),
    18: (-3122, 1.1156, 0),
    19: (310, 0.497648, 0),
    20: (3112, 1.19734, -1),
    21: (3222, 1.189, 1),
    22: (3212, 1.1926, 0),
    23: (111, 0.13498, 0),
    24: (311, 0.4977, 0),
    25: (-311, 0.497648, 0)
}



# Read in the event file and extract information about the primary  particles
def read_event_info(event_lines):
    ProjID = int(event_lines[0][17:30])
    ProjkE = float(event_lines[0][42:69])
    ProjdirX = float(event_lines[0][79:106])
    ProjdirY = float(event_lines[0][116:143])
    ProjdirZ = float(event_lines[0][153:180])
    Gen_No = int(event_lines[1][20:34])
    IntID = int(event_lines[2][17:31])
    NoSecondary = int(event_lines[3][32:57])

    return ProjID, ProjkE, ProjdirX, ProjdirY, ProjdirZ, Gen_No, IntID, NoSecondary

# Read in the secondary particles information  
def read_secondary_info(secondary_lines):

    IDs, Ps, Xs, Ys, Zs = [], [], [], [], []

    for secondary_line in secondary_lines:

        IDs += [int(secondary_line[10:24])]
        Ps += [float(secondary_line[36:64])]
        Xs += [float(secondary_line[73:101])]
        Ys += [float(secondary_line[110:138])]
        Zs += [float(secondary_line[147:174])]

    return np.array(IDs), np.array(Ps), np.array(Xs), np.array(Ys), np.array(Zs)

# Convert fluka userdump files into pandas dataframes
def FlukaDump_toPandas(fluka_dir, N_files, Energy):

    # Main loop to read files and extract data
    for i in np.arange(1,N_files+1,1):

        df = pd.DataFrame()

        # convert i to string with leading zeros
        i = str(i).zfill(3)
        # file name
        file_name = fluka_dir+"phiKK_"+str(Energy)+ i + "_fort.90"

        with open(file_name, "r") as file:
            lines = file.readlines()

        CurrentLine = 0
        TotLines = len(lines)

        while CurrentLine < TotLines:

            #Read current line
            line = lines[CurrentLine]

            if line[1:11] == 'PROJECTILE':

                ProjID, ProjkE, ProjdirX, ProjdirY, ProjdirZ, Gen_No, IntID, NoSecondary = read_event_info(lines[CurrentLine:CurrentLine+4])

                IDs, Ps, Xs, Ys, Zs = read_secondary_info(lines[CurrentLine+4:CurrentLine+4+NoSecondary])

                temp_df = pd.DataFrame({
                    'ProjID': [ProjID], 
                    'ProjkE': [ProjkE],
                    'ProjdirX': [ProjdirX],
                    'ProjdirY': [ProjdirY],
                    'ProjdirZ': [ProjdirZ],
                    'Gen_No': [Gen_No],
                    'IntID': [IntID],
                    'NoSecondary': [NoSecondary],
                    'IDs': [IDs],
                    'Ps': [Ps],
                    'Xs': [Xs],
                    'Ys': [Ys],
                    'Zs': [Zs]
                })

                # Append the temporary DataFrame to the main DataFrame
                df = pd.concat([df, temp_df], ignore_index=True)

                CurrentLine += 4 + NoSecondary  # Move to the next event block

            else:
                CurrentLine += 1

        df.to_pickle(fluka_dir+"phiKK_"+str(Energy)+ i + ".pkl")




# Function to convert FLUKA IDs to PDG IDs, masses, and charges
def convert_fluka_ids(ids):
    pdg_ids = []
    masses = []
    charges = []
    for id in ids:
        info = flukaIDdict.get(id, (None, None, None))  # Get tuple or a default tuple (None, None, None)
        pdg_ids.append(info[0])  # PDG ID
        masses.append(info[1])    # Mass
        charges.append(info[2])   # Charge
    return np.array(pdg_ids), np.array(masses), np.array(charges)




