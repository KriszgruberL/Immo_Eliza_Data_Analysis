from preprocessing.dataprocessor import DataProcessor
import pandas as pd


class Dataformat : 
    
    def __init__(self, df : pd.DataFrame) -> None :
        """
        Initializes the DataProcessor with data and DataFrame attributes set to None.
        """
        self.df = df

    def strip_blank(self)  -> None: 
        """
        Strips leading and trailing whitespace from all string columns.
        """
        for i in self.df.columns:
            # Check datatype for each column
            if self.df[i].dtype == "object": 
                self.df[i] = self.df[i].map(str.strip)
                self.df[i] = self.df[i].map(str.lower)
                self.df[i] = self.df[i].str.replace(" ", "_")
                
                

        