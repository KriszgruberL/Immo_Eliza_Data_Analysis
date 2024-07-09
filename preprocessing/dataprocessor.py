import datetime
from typing import List
import pandas as pd
import numpy as np


class DataProcessor:
    """
    A class used to process a dataset with various cleaning and preprocessing steps.
    """

    def __init__(self, data_path: str) -> None:
        """
        Initializes the DataProcessor with data and DataFrame attributes set to None.
        """
        self.data = data_path
        self.df = None

    def process(self) -> None:
        """
        Main method to execute all processing steps in sequence.
        """
        try:
            self.read()
            print("START: ", self.df.shape)
            self.check_coherence()
            self.drop_useless()
            self.fill_empty()
        except Exception as e:
            print(f"An error occurred during processing: {e}")

    def read(self) -> None:
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

    def drop_useless(self) -> None:
        """
        Drops duplicate rows and unnecessary columns, and removes rows with null values in critical columns.
        """
        self.df.drop_duplicates(inplace=True)
        self.df = self.df.drop(columns=["Country", "Fireplace"])  # Don't need those

        # List of columns where a missing value is not acceptable
        exclude = ["PostalCode", "Price", "PropertyId", "TypeOfProperty", "TypeOfSale"]
        self.df.dropna(
            subset=exclude, inplace=True
        )  # Drop rows where any of the exclude columns have null values

        self.df = self.df[self.df["PostalCodeValid"] == True]
        self.df.drop(columns=["PostalCodeValid"], inplace=True)

    def fill_empty(self) -> None:
        """
        Fills empty values in the DataFrame with appropriate default values.
        """
        default = {"numeric": 0, "string": "null"}
        # Update specific columns with appropriate empty values
        numeric_columns = [
            "BathroomCount",
            "BedroomCount",
            "ConstructionYear",
            "GardenArea",
            "LivingArea",
            "MonthlyCharges",
            "NumberOfFacades",
            "Price",
            "RoomCount",
            "ShowerCount",
            "SurfaceOfPlot",
            "SwimmingPool",
            "Terrace",
            "ToiletCount",
            "Furnished",
            "Garden",
        ]

        fill_values = {
            col: default["numeric"] if col in numeric_columns else default["string"]
            for col in self.df.columns
        }
        self.df.fillna(value=fill_values, inplace=True)

    def check_coherence(self) -> None:
        """
        Ensures data coherence by checking and adjusting certain columns' values.
        """
        year_threshold = datetime.datetime.today().year + 10

        # Keep rows where ConstructionYear is null or less than or equal to the year threshold
        self.df = self.df.loc[
            (self.df["ConstructionYear"] == "null")
            | (self.df["ConstructionYear"] <= year_threshold)
        ]

        # Drop rows where GardenArea is more than 0 and Garden is 0 (False)
        self.df = self.df.loc[~((self.df["GardenArea"] > 0) & (self.df["Garden"] == 0))]

        # Keep rows where LivingArea is between 9 and 2000
        self.df = self.df.loc[
            (self.df["LivingArea"] >= 9) & (self.df["LivingArea"] <= 2000)
        ]
        self.check_postal_code()

    def check_postal_code(self):
        self.postal_code = pd.read_json("data/zipcode-belgium.json")
        valid = set(self.postal_code["zip"])

        self.df["PostalCodeValid"] = self.df["PostalCode"].apply(lambda x: x in valid)

    def get_summary_stats(self) -> pd.DataFrame:
        """
        Returns summary statistics of the DataFrame.
        """
        return self.df.describe()

    def get_data(self) -> pd.DataFrame:
        """
        Returns the processed DataFrame.
        """
        return self.df

    def get_column(self) -> pd.Index:
        """
        Returns the columns of the DataFrame.
        """
        print(type(self.df.columns))
        return self.df.columns

    def save(self) -> None:
        """
        Saves the processed DataFrame to a CSV file.
        """
        try:
            self.df.to_csv("data/dataset1.csv")
            print("END: ", self.df.shape)
            print("Done!")
        except Exception as e:
            print(f"An error occurred while saving the data: {e}")
            raise
