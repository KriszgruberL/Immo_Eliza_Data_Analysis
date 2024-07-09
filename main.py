from preprocessing.dataprocessor import DataProcessor


def main():
    """
    Main function to create an instance of DataProcessor and execute the processing steps.
    """
    processor = DataProcessor()
    processor.process()

    print("********************")
    print("********************")
    print(processor.get_data().head())
    print(processor.get_column())
    print(processor.get_summary_stats())

if __name__ == "__main__":
    main()