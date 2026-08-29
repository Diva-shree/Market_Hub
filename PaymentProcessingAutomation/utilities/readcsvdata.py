import csv
import os


class ReadCSVData:

    @staticmethod
    def read_data_from_csv(filename):

        # Create empty list
        data_list = []

        # Get project root directory
        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        # Create complete path of CSV file
        file_path = os.path.join(
            base_dir,
            filename
        )

        # Open CSV file
        with open(file_path, "r") as csv_data:

            # Create CSV reader
            reader = csv.reader(csv_data)

            # Skip header
            next(reader)

            # Read each row
            for rows in reader:

                # Add row to list
                data_list.append(rows)

        # Return all data
        return data_list
