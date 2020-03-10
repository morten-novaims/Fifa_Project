import pandas as pd
import numpy as np


positions = ['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
       'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM',
       'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB']

def get_random_state(seed):
    return np.random.RandomState(seed)

def data_import(normalized_positions=True):
    #import data as pd dataframe
    data = pd.read_csv("Data_Files/data.csv")
    data.drop("Unnamed: 0", axis=1, inplace=True)
    data = data.loc[:, ["ID", "Overall", "Position", "Value", "Age", "Potential"] + positions]
    data.dropna(axis=0, inplace=True, subset=["ID", "Overall", "Position", "Value", "Age", "Potential"])
    data["Potential_Gain"] = data["Potential"] - data["Overall"]
    data["Value"] = data["Value"].apply(normalize_values)
    data = data.loc[data["Value"]>0,:]

    for position in positions:
        data[position] = data[position].apply(normalize_position_values)

    if normalized_positions:
        data["Normalized_Position"] = data["Position"].apply(normalize_position)
        data.drop(["Position"], axis=1, inplace=True)

    return data


def player_import():
    data = pd.read_csv("Data_Files/data.csv")
    data.drop("Unnamed: 0", axis=1, inplace=True)
    data["Potential_Gain"] = data["Potential"] - data["Overall"]
    data = data.loc[:, ["ID", "Name", "Overall", "Value", "Position", "Age", "Potential_Gain"]]
    return data


def normalize_position(position):
    # Goali
    if position == "GK":
        return "GK"
    # Defenders: RCB, CB, LCB, LB, RB, RWB, LWB
    elif "B" in position:
        return "DEF"
    # Midfielders: RCM, LCM, LDM, CAM, CDM, RM, LAM, LM, RDM, RW, CM, RAM, LW
    elif "M" in position or "W" in position:
        return "MID"
    # Attackers: RF, ST, LF, RS, LS, CF
    elif "S" in position or "F" in position:
        return "ST"
    else:
        return


def normalize_values(value):
    value = value.replace("€", "")
    if "M" in value:
        value = value.replace("M", "")
        return float(value)
    if "K" in value:
        value = value.replace("K", "")
        value = float(value)
        return value/1000
    return None


def normalize_position_values(x):
    if type(x) == str:
        return int(x[:2]) + int(x[3:])
    else:
        return x
