import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def load_sloth():

    """ FUNCTION ADD_NEW_SLOTHS: Loads in sloth meta data. The default file loaded isname is "sloth_data.csv". 
    Updated data is tagged with a datestamp in the format "%Y%m%d_%H%M%S". If available, the function will preferrentially
    load updated data. 
    """

    #for debugging
    #hostpath = 'data'
    hostpath = '/opt/airflow/data'

    #initialize lists
    sloth_files = []
    file_datetime = []

    #build list of available sloth datasets
    for path in Path(hostpath).glob("sloth_*.csv"):
        sloth_files.append(path)

    #split to parse datestamp and convert to python datetime object in a list
    for file in sloth_files:
        file = file.__str__()[:-4]
        splitname = file.split('_')

        if any(i.isdigit() for i in splitname):
            file_date = splitname[1] + '_' + splitname[2]
            file_datetime.append(datetime.strptime(file_date, "%Y%m%d_%H%M%S"))

    #if no datestamps, then load the default filename. Else sort and load most recent
    if not file_datetime:
        sloths = pd.read_csv(hostpath + '/sloth_data.csv', encoding='utf-8')
    else:
        file_datetime.sort(reverse=True)
        newest_string = file_datetime[0].strftime('%Y%m%d_%H%M%S')
        sloths = pd.read_csv(hostpath + '/sloth_' + newest_string +'.csv', encoding='utf-8')


    #drop unnecessary columns and one hot encode the remaining
    if 'Unnamed: 0' in sloths:
        to_drop_sloth = ['Unnamed: 0','endangered','specie','sub_specie']
    else:
        to_drop_sloth = ['endangered','specie','sub_specie']
    sloths_X = sloths.drop(to_drop_sloth,axis=1)
    sloths_y = sloths['specie']

    if 'Unnamed: 0' in sloths:
        to_drop_sloth_non_dummies = ['Unnamed: 0','endangered','sub_specie', 'claw_length_cm', 'size_cm', 'tail_length_cm', 'weight_kg']
    else:
        to_drop_sloth_non_dummies = ['endangered','sub_specie', 'claw_length_cm', 'size_cm', 'tail_length_cm', 'weight_kg']

    sloth_dummies = pd.get_dummies(sloths, columns=['specie'])
    sloths_y = sloth_dummies.drop(to_drop_sloth_non_dummies,axis=1)

    if 'Unnamed: 0' in sloths:
        #keep copy of original (minus one column)
        to_drop_sloth_orig = ['Unnamed: 0']
        sloths = sloths.drop(to_drop_sloth_orig,axis=1)

    return sloths, sloths_X, sloths_y