import numpy as np
import pandas as pd 


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
