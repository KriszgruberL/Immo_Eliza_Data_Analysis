from preprocessing.dataformat import Dataformat
from preprocessing.dataprocessor import DataProcessor


def main():
    """
    Main function to create an instance of DataProcessor and execute the processing steps.
    """
    data = "data/final_dataset.json"
    p = DataProcessor(data)
    
    
    p.process()
    
    f = Dataformat(p.get_data())
    f.strip_blank()
    
    p.save()

    print(p.get_data().head())
    print(p.get_column())
    print(p.get_summary_stats())

if __name__ == "__main__":
    main()