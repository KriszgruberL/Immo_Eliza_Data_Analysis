from preprocessing.dataprocessor import DataProcessor


def main():
    """
    Main function to create an instance of DataProcessor and execute the processing steps.
    """
    processor = DataProcessor()
    processor.process()


if __name__ == "__main__":
    main()