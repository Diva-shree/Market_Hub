import csv
import os


class ReadCSVData:

    @staticmethod
    def read_data_from_csv(filename):

        data_list = []

        # Get project root directory
        base_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        # Create complete CSV file path
        file_path = os.path.join(base_dir, "testdata", filename)

        # Open CSV file
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                data_list.append(row)

        return data_list
