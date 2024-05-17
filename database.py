import pickle
from dotenv import load_dotenv, set_key
import os
import csv

class Database():

    def __init__(self):
        self.measurements_sets_list = []
        self.database_path = ""


    def save_database(self):

        if self.database_path == "":
            self.database_path = 'database.obj'
            set_key('.env', 'DATABASE_PATH', self.database_path)

        with open(self.database_path, 'wb') as file:
            pickle.dump(self, file)
        file.close()


    @staticmethod
    def load_database(file_name: str):

        with open(file_name, 'rb') as file:
            return pickle.load(file)

    @staticmethod
    def load_database_path():

        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(dotenv_path, override=True)

        try:

            return os.getenv('DATABASE_PATH')
        
        except:
            raise ValueError(".env file not found in program directory")

    @staticmethod
    def switch_database(existing_database_path: str):

        try:

            with open(existing_database_path, 'rb') as file:
                existing_database = pickle.load(file)
            file.close()
        
        except:
            input("File, not found, creating new database, press enter to continue:")
            return Database()

        if isinstance(existing_database, Database):
            return existing_database
        
        else:
            input("Existing database is not an instance of Database, creating new database, press enter to continue:")
            return Database()



    def delete_database(self):
            
            if os.path.exists(self.database_path):
                os.remove(self.database_path)
                self.database_path = ""
                set_key('.env', 'DATABASE_PATH', "")
            else:
                pass


    def change_database_path(self, new_path: str):

        self.database_path = new_path
        set_key('.env', 'DATABASE_PATH', new_path)


    def print_measurements_sets(self):

        for index, measurement_set in enumerate(self.measurements_sets_list):
            print(f'{index+1}. {measurement_set.measurements_name}')


    def add_measurement_set(self, measurement_set):

        if isinstance(measurement_set, MeasurementSet):
            self.measurements_sets_list.append(measurement_set)

        else:
            raise ValueError("Measurement set must be an instance of MeasurementSet")

    
    def delete_measurement_set(self, measurement_sets: list):

        for measurement_set in measurement_sets:
            
            if measurement_set in self.measurements_sets_list:
                self.measurements_sets_list.remove(measurement_set)

            else:
                raise ValueError("Measurement set not in list")
        

class MeasurementSet():


    def __init__(self, measurements_set_name: str):
            
        if not isinstance(measurements_set_name, str):
            raise ValueError("Measurement set name must be a string")

        self.measurements_name = measurements_set_name
        self.measurements_list = []


    def __str__(self):
        return f"{self.measurements_name}"
        

    def add_measurement(self, measurement):

        self.measurements_list.append(measurement)


    def delete_measurement(self, measurements: list):

        for measurement in measurements:
            
            if measurement in self.measurements_list:
                self.measurements_list.remove(measurement)

            else:
                raise ValueError("Measurement not in list")
        

    def print_measurements(self):
        
        headers = ["Number", "Calculation name", "Scenario", "Line of sight", "Frequency", "Distance", 
                "Heigth of Base Station", "Heigth of Media Station", "Length of Grid(d1)", 
                "Width of Grid(d2)", "Street Width(w)", "Result"]
        print(' | '.join(f"{h:<{len(h)}}" for h in headers))
        for index, measurement in enumerate(self.measurements_list):
            
            print(f"{index+1:<{len(headers[0])}} | {measurement.print_in_list()}")


    def export_to_csv(self, ):

        line_data = []
        headers = ["Calculation name", "Scenario", "Line of sight", "Frequency", "Distance", 
                "Heigth of Base Station", "Heigth of Media Station", "Length of Grid(d1)", 
                "Width of Grid(d2)", "Street Width(w)", "Result"]
        
        line_data.append(headers)

        for measurement in self.measurements_list:
            line_data.append(measurement.export_to_list())

        with open(f"{self.measurements_name}.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(line_data)
