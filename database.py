# from calculations import WinnerCalculator
import inquirer
import inquirer.errors

class Database():

    measurements_sets_list = []


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
        

    def get_measuremenmts_from_file(self, file_name: str): #TODO

        pass


    def add_measurement(self, measurement):


        self.measurements_list.append(measurement)
        # if isinstance(measurement, WinnerCalculator):
        #     self.measurements_list.append(measurement)

        # else:
        #     raise ValueError("Measurement must be an instance of WinnerCalculator")


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


