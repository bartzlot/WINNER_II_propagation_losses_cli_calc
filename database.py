from calculations import WinnerCalculator
# class Database():

#     measurements_sets_list = []


class MeasurementSet():

    measurements_list = []
    measurements_set_name = ""


    def __str__(self):
        return f"\n".join(f"{i} | {str(measurement)}" for i, measurement,  in enumerate(self.measurements_list))
        

    def add_measurement(self, measurement):

        if isinstance(measurement, WinnerCalculator):
            self.measurements_list.append(measurement)

        else:
            raise ValueError("Measurement must be an instance of WinnerCalculator")


    def delete_measurement(self, measurement):

        if measurement in self.measurements_list:
            self.measurements_list.remove(measurement)

        else:
            raise ValueError("Measurement not in list")


