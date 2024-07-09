import datetime
import pandas as pd
import numpy as np

class DataProcessor:
    """
    A class used to process a dataset with various cleaning and preprocessing steps.
    """
    def __init__(self):
        """
        Initializes the DataProcessor with data and DataFrame attributes set to None.
        """
        self.data = None
        self.df = None
        
    def process(self) : 
        """
        Main method to execute all processing steps in sequence.
        """
        try:
            self.read()
            print("START: ", self.df.shape)
            self.drop_useless()
            self.check_coherence()
            self.fill_empty()
            self.strip_blank()
            self.save()
            print("END: ", self.df.shape)
            self.view()
            print("Done!")
        except Exception as e:
            print(f"An error occurred during processing: {e}")
        
    def view(self) :
        """
        Prints the first few rows, columns, and descriptive statistics of the DataFrame.
        """ 
        print(self.df.head())
        print(self.df.columns)
        print(round(self.df.describe(), 2))

              
    def read(self): 
        """
        Reads the dataset from a JSON file and initializes the DataFrame.
        """
        try: 
            self.data = pd.read_json("data/final_dataset.json")
            self.df = pd.DataFrame(self.data)
        except FileNotFoundError as e: 
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred while reading the data: {e}")
        
        
    def drop_useless(self) : 
        """
        Drops duplicate rows and unnecessary columns, and removes rows with null values in critical columns.
        """
        self.df.drop_duplicates(inplace=True)
        self.df = self.df.drop(columns = ["Country", "Fireplace"]) # Don't need those 
        
        # List of columns where a missing value is not acceptable
        exclude = ["PostalCode", "Price", "PropertyId", "TypeOfProperty", "TypeOfSale"]
        self.df.dropna(subset=exclude, inplace=True) # Drop rows where any of the exclude columns have null values
            
    def fill_empty(self): 
        """
        Fills empty values in the DataFrame with appropriate default values.
        """
        default = {'numeric': 0, 'string': "null"}
        # Update specific columns with appropriate empty values
        numeric_columns = ['BathroomCount', 'BedroomCount', 'ConstructionYear', 'GardenArea', 
                           'LivingArea', 'MonthlyCharges', 'NumberOfFacades', 'Price', 
                           'RoomCount', 'ShowerCount', 'SurfaceOfPlot', 'SwimmingPool', 
                           'Terrace', 'ToiletCount', 'Furnished', 'Garden']

        fill_values = {col: default['numeric'] if col in numeric_columns else default['string'] for col in self.df.columns}
        self.df.fillna(value=fill_values, inplace=True)

    def check_coherence(self): 
        """
        Ensures data coherence by checking and adjusting certain columns' values.
        """
        year_threshold = datetime.datetime.today().year + 10

         # Keep rows where ConstructionYear is null or less than or equal to the year threshold
        self.df = self.df.loc[(self.df['ConstructionYear'] == 'null') | (self.df['ConstructionYear'] <= year_threshold)]
        
        # Drop rows where GardenArea is more than 0 and Garden is 0 (False)
        self.df = self.df.loc[~((self.df['GardenArea'] > 0) & (self.df['Garden'] == 0))]
        
        # Keep rows where LivingArea is between 9 and 2000
        self.df = self.df.loc[(self.df['LivingArea'] >= 9) & (self.df['LivingArea'] <= 2000)]


    def strip_blank(self): 
        """
        Strips leading and trailing whitespace from all string columns.
        """
        for i in self.df.columns:
            # Check datatype for each column
            if self.df[i].dtype == "object": 
                self.df[i] = self.df[i].map(str.strip)
                
    def save(self) : 
        """
        Saves the processed DataFrame to a CSV file.
        """
        try:
            self.df.to_csv("data/dataset1.csv")
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")
            raise
