from preprocessing.dataprocessor import DataProcessor


def main():
    processor = DataProcessor()
    processor.read()
    processor.drop_useless()
    processor.check_coherence()
    processor.fill_empty()
    processor.strip_blank()
    processor.save()

if __name__ == "__main__":
    main()