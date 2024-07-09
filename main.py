
from preprocessing.df_splitter import DataFrameSplitter
from preprocessing.clean_data import CleanData



def main():
    """
    Main function to create an instance of DataProcessor and execute the processing steps.
    """
    data_path = "data/final_dataset.json"
    zip_path = "data/zipcode-belgium.json"
    save_path = "data/clean_dataset.csv"
    
    p = CleanData(data_path, zip_path, save_path)
    p.process()
    
    
    splitter = DataFrameSplitter()
    splitter.split_and_save(p.get_data())

    # print(p.get_data().head())
    # print(p.get_column())git 
    # print(p.get_summary_stats())
    
    

if __name__ == "__main__":
    main()