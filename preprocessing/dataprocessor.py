import datetime
import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self):
        self.data = None
        self.df = None
        
    def read(self): 
        self.data = pd.read_json("data/final_dataset.json")
        self.df = pd.DataFrame(self.data)
        
    def drop_useless(self) : 
        self.df.drop_duplicates(inplace=True)
        self.df = self.df.drop(columns = ["Country", "Fireplace"])
            
    def fill_empty(self): 
        default = {'numeric': 0, 'string': "null"}
        # Update specific columns with appropriate empty values
        numeric_columns = ['BathroomCount', 'BedroomCount', 'ConstructionYear', 'GardenArea', 
                           'LivingArea', 'MonthlyCharges', 'NumberOfFacades', 'Price', 
                           'RoomCount', 'ShowerCount', 'SurfaceOfPlot', 'SwimmingPool', 
                           'Terrace', 'ToiletCount', 'Furnished', 'Garden']

        fill_values = {col: default['numeric'] if col in numeric_columns else default['string'] for col in self.df.columns}
        fill_values['ConstructionYear'] = "null"  

        self.df.fillna(value=fill_values, inplace=True)

    def check_coherence(self): 
        year_threshold = datetime.datetime.today().year + 10

        # Ensure 'ConstructionYear' column is of numeric type, but keep 'null' as it is
        self.df.loc[self.df['ConstructionYear'] != 'null', 'ConstructionYear'] = pd.to_numeric(self.df.loc[self.df['ConstructionYear'] != 'null', 'ConstructionYear'], errors='coerce')
        
        self.df = self.df.loc[(self.df['ConstructionYear'] == 'null') | (self.df['ConstructionYear'] <= year_threshold)]
        self.df = self.df.loc[~((self.df['GardenArea'] > 0) & (self.df['Garden'] == 0))]
        self.df = self.df.loc[self.df['LivingArea'] >= 9]


    def strip_blank(self): 
        for i in self.df.columns:
            # Check datatype for each column
            if self.df[i].dtype == "object": 
                self.df[i] = self.df[i].map(str.strip)
                
    def save(self) : 
        self.df.to_csv("data/dataset1.csv")
        print("Done!")