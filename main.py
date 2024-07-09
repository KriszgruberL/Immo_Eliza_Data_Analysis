
from preprocessing.preprocessor import DataProcessor


def main():
    """
    Main function to create an instance of DataProcessor and execute the processing steps.
    """
    data_path = "data/final_dataset.json"
    p = DataProcessor(data_path)
    p.process()


    p.save()

    print(p.get_data().head())
    print(p.get_column())
    print(p.get_summary_stats())

if __name__ == "__main__":
    main()