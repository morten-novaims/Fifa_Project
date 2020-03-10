import utils as utls
import pandas as pd

def show_squad(player_id):
    data = utls.player_import()
    columns = ["Name", "Overall", "Value", "Position", "Age", "Potential_Gain"]
    names = pd.DataFrame(columns = columns)
    for i, id in enumerate(player_id):
        name = data.loc[data["ID"] == id, columns]
        names = names.append(name)
    names = [tuple(x) for x in names.values]
    print("---------{} ------".format(names[0]))
    print()
    print("--%s-- %s-- %s-- %s--" % (names[1], names[2], names[3], names[4]))
    print()
    print("--%s-- %s-- %s-- %s--" % (names[5], names[6], names[7], names[8]))
    print()
    print("------%s-- %s-------" % (names[9], names[10]))
    return names