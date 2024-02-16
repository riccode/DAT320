from utils.load_sloth import load_sloth
import pandas as pd
import numpy as np
from datetime import datetime
import random

def add_new_sloths():

    """ FUNCTION ADD_NEW_SLOTHS: Adds in a new randomly generated sloth species to the dataset. A new file is created with 
    the new data and the filename is appended with a timestamp. Usually this would be done in a database. But this solution is
    sufficient for this project. 
    """
        
    #load in sloth data    
    sloths, sloths_X, sloths_y = load_sloth()

    #all columns of the sloth dataset
    df_columns = ['claw_length_cm', 'endangered', 'size_cm', 'specie', 'sub_specie', 'tail_length_cm', 'weight_kg']

    #get current timestamp
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    #measurements of a possible new sloth species
    #tail length 8-10
    #size 65-80
    #claw length 6-9
    #weight 8-12

    #randomize ranges for new sloth species
    tail_range = sorted([random.randint(1, 10), random.randint(1, 10)])
    size_range = sorted([random.randint(30, 80), random.randint(30, 80)])
    claw_range = sorted([random.randint(1, 12), random.randint(1, 12)])
    weight_range = sorted([random.randint(1, 12), random.randint(1, 12)])

    #also randomize sample size of data
    random_size = random.randint(1000, 2500)

    #write new data fields to a pandas series
    tail_length=pd.Series(np.random.uniform(low=tail_range[0], high=tail_range[1], size=random_size))
    sloth_size=pd.Series(np.random.uniform(low=size_range[0], high=size_range[1], size=random_size))
    claw_length=pd.Series(np.random.uniform(low=claw_range[0], high=claw_range[1], size=random_size))
    sloth_weight=pd.Series(np.random.uniform(low=weight_range[0], high=weight_range[1], size=random_size))

    #build new dataset dataframe
    update_df = pd.DataFrame([], columns = [df_columns])
    update_df['claw_length_cm'] = claw_length
    update_df['endangered'] = 'thriving'
    update_df['size_cm'] = sloth_size
    update_df['specie'] = 'DAT320_sloth_' + str(np.random.randint(10000))
    update_df['sub_specie'] = 'sloth_' + str(np.random.randint(10000))
    update_df['tail_length_cm'] = tail_length
    update_df['weight_kg'] = sloth_weight

    update_df.columns = sloths.columns

    #merge new dataset the old one and write to file
    df_merged = pd.concat([sloths, update_df], sort=False)
    df_merged.to_csv('/opt/airflow/data/sloth_' + now + '.csv' , sep=',', index=False) 

