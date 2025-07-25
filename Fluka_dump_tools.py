import numpy as np
import pandas as pd 
import os

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
def Fluka2Pandas(file_path):
    
    # Open fluka fort.90 dump file and read lines
    with open(file_path, "r") as file:
            lines = file.readlines()

    # Loop through the lines of the file and add information to pandas datafram
    df = pd.DataFrame()
    CurrentLine = 0
    TotLines = len(lines)
    while CurrentLine < TotLines:

        #Read current line
        line = lines[CurrentLine]

        if line[1:11] == 'PROJECTILE':

            ProjID, ProjkE, ProjdirX, ProjdirY, ProjdirZ, Gen_No, IntID, NoSecondary = read_event_info(lines[CurrentLine:CurrentLine+4])

            IDs, Ps, Xs, Ys, Zs = read_secondary_info(lines[CurrentLine+4:CurrentLine+4+NoSecondary])

            df_row = pd.DataFrame({
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
                'dir_xs': [Xs],
                'dir_ys': [Ys],
                'dir_zs': [Zs]
            })

            # Add row to the dataframe
            df = pd.concat([df, df_row], ignore_index=True)

            CurrentLine += 4 + NoSecondary  # Move to the next event block

        else: CurrentLine += 1

    return df

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


def find_files_with_extension(path, extension):
    
    # List to hold the matching file paths
    files_with_extension = []

    # Check if the specified path is a directory
    if not os.path.isdir(path):
        raise ValueError(f"The provided path '{path}' is not a valid directory.")

    # List all files in the specified directory
    for file in os.listdir(path):
        # Construct the full file path
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path) and file.endswith(extension):
            files_with_extension.append(file_path)

    return files_with_extension

def write_lhe(df, output_dir, output_name, include_recoil_e = False, include_other_secondaries = False, elastic_only = False):

    if elastic_only:
        df = df.loc[df.NoSecondary == 2].reset_index(drop=True)


    # Create lhe file and add header
    file = open(output_dir+'/'+output_name, "w")


    rscale = 1.740000e+02
    alpha_EM = 7.297353e-03  # Fine-structure constant
    alpha_QCD = 1.078706E-01
    beam_energy = 4.5

    #Write header 
    file.write(f"\n")

    file.write(f"<LesHouchesEvents version=\"3.0\">\n")
    file.write(f"<header>\n")
    file.write(f"#  Number of Events        :       "+str(len(df))+"\n")
    file.write(f"</header>\n")

    # Write the body of the LHE file
    file.write(f"<init>\n")
    file.write(f"{11} {623} {beam_energy:.6e} {rscale:.6e} {0} {0} {0} {0} {0} {1}\n")
    file.write("0 0 0 1\n")
    file.write(f"</init>\n")


    # Loop through the DataFrame and write the lines to the file
    for index, row in df.iterrows():

        # Start event block
        file.write(f"<event>\n")


        if include_other_secondaries and include_recoil_e:
            file.write(f"{1+row['NoSecondary']:>2}{1:>7} {0} {rscale:.8e} {alpha_EM:.8e} {alpha_QCD:.8e} \n")
        elif include_other_secondaries and (include_recoil_e == False):
            file.write(f"{row['NoSecondary']:>2}{1:>7} {0} {rscale:.8e} {alpha_EM:.8e} {alpha_QCD:.8e} \n")
        elif (include_other_secondaries == False) and (include_recoil_e):
            file.write(f"{3:>2}{1:>7} {0} {rscale:.8e} {alpha_EM:.8e} {alpha_QCD:.8e} \n")
        else:
            file.write(f"{2:>2}{1:>7} {0} {rscale:.8e} {alpha_EM:.8e} {alpha_QCD:.8e} \n")

        # Include recoil electron if specified
        if include_recoil_e:
            file.write(f"{11:>9}{1:>3}{0:>5}{0:>5}{0:>5}{0:>5}{-row.ProjkE*row.ProjdirX:>+18.10e}{-row.ProjkE*row.ProjdirY:>+18.10e}{beam_energy-row.ProjkE*row.ProjdirZ:>+18.10e}{beam_energy-row.ProjkE:>17.10e}{5.11E-4:>17.10e}{0:>11.4e} {1:>.4e}\n")

        # Now include the secondaries
        for PDG_ID, P, x, y, z, m, c in zip(row.PDG_IDs,row.Ps,row.dir_xs,row.dir_ys,row.dir_zs, row.Sec_mass, row.Sec_charge):

            # Inlcude all secondaries if specified
            if include_other_secondaries:
                if m != 0:  #If it's not a Photon E= m/sqrt(1-P^2/(P^2 + m^2))
                    file.write(f"{PDG_ID:>9}{1:>3}{0:>5}{0:>5}{0:>5}{0:>5}{P*x:>+18.10e}{P*y:>+18.10e}{P*z:>+18.10e}{m/np.sqrt(1-P**2/(m**2+P**2)):>17.10e}{m:>17.10e}{0:>11.4e} {0:>.4e}\n")
                else:       #If it is a Photon E = P 
                    file.write(f"{PDG_ID:>9}{1:>3}{0:>5}{0:>5}{0:>5}{0:>5}{P*x:>+18.10e}{P*y:>+18.10e}{P*z:>+18.10e}{P:>17.10e}{m:>17.10e}{0:>11.4e} {0:>.4e}\n")
            
            # Otherwise only include the charged kaons
            elif (PDG_ID == 321) or (PDG_ID == -321):
                file.write(f"{PDG_ID:>9}{1:>3}{0:>5}{0:>5}{0:>5}{0:>5}{P*x:>+18.10e}{P*y:>+18.10e}{P*z:>+18.10e}{m/np.sqrt(1-P**2/(m**2+P**2)):>17.10e}{m:>17.10e}{0:>11.4e} {0:>.4e}\n")

        # end event block
        file.write(f"</event>\n")

    file.write(f"</LesHouchesEvents>")
    file.close()
    print("LHE written to: ", output_dir+'/'+output_name)
