import datetime
from typing import Dict, List
import pandas as pd
import numpy as np

from preprocessing.categorical_to_num_dict import CategoricalNumDict
from utils.save_read import save_df_to_csv

class Preprocessing : 
    def __init__(self) -> None:
        pass 
    
    def transform_categorical(self, df : pd.DataFrame, dict_key : str, dicts : CategoricalNumDict) -> pd.DataFrame:
        df_to_return = df.copy()
        mapping_dict = dicts.get_dict(dict_key)
        
        if mapping_dict is None:
            raise ValueError(f"No dictionary found for key: {dict_key}")
    
        df_to_return.loc[:, f'{dict_key}'] = df_to_return[f'{dict_key}'].map(mapping_dict)
        df_to_return = df_to_return.dropna(subset=[f'{dict_key}'])
        
        save_df_to_csv(df_to_return, f"data/{dict_key}.csv")
    
        return df_to_return
        

    def transform(self, df : pd.DataFrame) -> pd.DataFrame:
        df_peb = df.copy()
        
        df_temp = df["FloodingZone"].unique()
        print(df_temp)
        
    
        # # df_peb.loc[ :, 'PEB_num'] = df_peb["PEB"].map(peb_dict)
        # df_peb.loc[:, 'PEB'] = df_peb["PEB"].map(peb_dict)
        # df_peb = df_peb.dropna(subset=['PEB'])
        
        return df_peb