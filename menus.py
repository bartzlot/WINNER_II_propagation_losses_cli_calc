import inquirer
import inquirer.errors
from os import name, system
from os.path import realpath
from database import MeasurementSet


def main_menu():

    clear_screen()
    questions = [
        inquirer.List('main_menu', message="WINNER II Calculator (choose an option using arrow keys)", 
                      choices=['Calculate Winner Model', 'Measurement sets', 'Database options', 'Exit'])
    ]
    answers = inquirer.prompt(questions)

    return answers['main_menu']


class MenuEngine: #TODO export to csv option

    def __init__(self, *args):
        
        self.menu_listing = args


    def run_menus(self):

        self.menu_running = 0

        while True:
                
                clear_screen()

                if isinstance(self.menu_listing[self.menu_running], ConditionalInput):

                    self.menu_listing[self.menu_running].line_of_sight = self.menu_listing[2].answers['line_of_sight']
                    self.menu_listing[self.menu_running].scenario = self.menu_listing[1].answers['scenario']

                choice = self.menu_listing[self.menu_running].get_input()

                if isinstance(self.menu_listing[self.menu_running], MeasurementsSetMenu):

                    if choice == 'Add measurement set':

                        measurement_set = MeasurementSet(measurement_set_input())
                        self.menu_listing[self.menu_running].measurements_set_database.add_measurement_set(measurement_set)
                        self.menu_listing[self.menu_running].measurements_set_database.save_database()
                        continue

                    elif choice == 'Delete measurement set':
                        
                        measurement_sets_list = self.menu_listing[self.menu_running].measurements_set_database.measurements_sets_list

                        if not measurement_sets_list:
                            custom_error_message("There is no measurement set to delete. Press Enter to continue")
                            continue
                        
                        measurement_chosen_list = self.menu_listing[self.menu_running].choose_measurement_set(measurement_sets_list)
                        self.menu_listing[self.menu_running].measurements_set_database.delete_measurement_set(measurement_chosen_list)
                        self.menu_listing[self.menu_running].measurements_set_database.save_database()
                        continue
                    
                    elif choice == 'View measurement set':

                        measurement_sets_list = self.menu_listing[self.menu_running].measurements_set_database.measurements_sets_list

                        if not measurement_sets_list:
                            custom_error_message("There is no measurement set to view. Press Enter to continue")
                            continue
                                
                        measurement_chosen = self.menu_listing[self.menu_running].choose_view_measurement_set(measurement_sets_list)
                        self.menu_listing[self.menu_running + 1].measurement_set_instance = measurement_chosen

                if isinstance(self.menu_listing[self.menu_running], MeasurementsViewMenu):

                    if choice == 'Delete measurement':

                        measurements_list = self.menu_listing[self.menu_running].measurement_set_instance.measurements_list

                        if not measurements_list:
                            custom_error_message("There is no measurement to delete. Press Enter to continue")
                            continue

                        measurement_chosen_list = self.menu_listing[self.menu_running].choose_measurement(measurements_list)
                        continue

                if choice == 'Main menu':
                    return False
    
                elif choice == 'Back':

                    if self.menu_running == 0:
                        return False

                    self.menu_running -= 1
    
                else:
                    
                    if self.menu_running == len(self.menu_listing) - 1:
                        break
                    self.menu_running += 1

        return True


class DatabaseOptionsMenu:


    def __init__(self, current_database_path: str):

        self.database_path = current_database_path
        self.answers = None
        self.questions = [
            inquirer.List('database_options', message="Choose an option", 
                          choices=['Switch Database', 'Edit database path', 'Create new database','Back'])
        ]


    def get_input(self):

        print(f"Current database path: {(self.database_path)}")
        self.answers = inquirer.prompt(self.questions)
        return self.answers['database_options']


    def new_path_input(self):

        clear_screen()
        questions = [
            inquirer.Text('new_path', message="Enter the new path to the database", validate=validate_path)
        ]
        answers = inquirer.prompt(questions)
        self.database_path = answers['new_path']

        return answers['new_path']
    

class DefaultValuesInput:
    
        def __init__(self):
            self.answers = None
            self.questions = [
                inquirer.Text('measurement_name', message="Enter the name of the measurement", validate=validate_name),
                inquirer.Text('frequency', message="Enter the frequency (GHz)",validate=validate_number),
                inquirer.Text('distance', message="Enter the distance (m)",validate=validate_number),
                inquirer.Text('res_round', message="Enter the number of decimal places to round the result",validate=validate_round),
            ]
    
        def get_input(self):

            if self.answers is None:
                self.answers = inquirer.prompt(self.questions)
                confirm = values_confirmation(self.answers)

            else:
                confirm = values_confirmation(self.answers)

            return confirmation_condition(confirm, self.answers)
        

class MeasurementsSetMenu:


    def __init__(self, measurements_set_database: object):

        self.measurements_set_database = measurements_set_database
        self.answers = None
        self.questions = [
            inquirer.List('measurements_set_menu', message="Choose an option", 
                          choices=['View measurement set', 'Add measurement set', 'Delete measurement set', 'Export to .csv', 'Back', 'Main menu'])
        ]


    def get_input(self):
        
        self.measurements_set_database.print_measurements_sets()
        self.answers = inquirer.prompt(self.questions)

        return self.answers['measurements_set_menu']
    

    def update_database(self, new_database_obj: object):
        self.measurements_set_database = new_database_obj


    def choose_measurement_set(self, measurement_sets_list: list):

        clear_screen()
        questions = [
            inquirer.Checkbox('measurements_set', message="Choose a measurement set", choices=measurement_sets_list)
        ]
        answers = inquirer.prompt(questions)

        return answers['measurements_set']
    

    def choose_view_measurement_set(self, measurement_sets_list: list):

        clear_screen()
        questions = [
            inquirer.List('measurements_set', message="Choose a measurement set", choices=measurement_sets_list)
        ]
        answers = inquirer.prompt(questions)

        return answers['measurements_set']
    

class MeasurementsViewMenu:


    def __init__(self):
        
        self.measurement_set_instance = None
        self.answers = None
        self.questions = [
            inquirer.List('measurements_view_menu', message="Choose an option", 
                          choices=['Delete measurement', 'Back', 'Main menu'])
        ]


    def get_input(self):

        self.measurement_set_instance.print_measurements()
        self.answers = inquirer.prompt(self.questions)

        return self.answers['measurements_view_menu']


    def choose_measurement(self, measurements_list: list):

        clear_screen()
        measurements_dict = {measurement.print_in_list(): measurement for measurement in measurements_list}
        questions = [
            inquirer.Checkbox('measurements', message="Choose a measurements", choices=list(measurements_dict.keys()))
        ]
        answers = inquirer.prompt(questions)

        self.measurement_set_instance.delete_measurement(measurements_dict[key] for key in answers['measurements'])


class ScenarioInput:

    def __init__(self):
        self.answers = None
        self.questions = [
            inquirer.List('scenario', message="Choose a scenario", choices=['B1', 'C2', 'D1'])
        ]

    def get_input(self):

        self.answers = inquirer.prompt(self.questions)
        confirm = values_confirmation(self.answers['scenario'])
        
        return confirmation_condition(confirm, self.answers['scenario'], values_list=['B1', 'C2', 'D1'])
    
    def edit_input(self):

        confirm = values_confirmation(self.answers['scenario'])
    
        return confirmation_condition(confirm, self.answers['scenario'], values_list=['B1', 'C2', 'D1'])
    

class LineOfSightInput:

    def __init__(self):
        self.answers = None
        self.questions = [
            inquirer.List('line_of_sight', message="Choose a line of sight", choices=['LOS', 'NLOS'])
        ]

    def get_input(self):

        self.answers = inquirer.prompt(self.questions)
        confirm = values_confirmation(self.answers['line_of_sight'])
    
        return confirmation_condition(confirm, self.answers['line_of_sight'], values_list=['LOS', 'NLOS'])
    
    def edit_input(self):

        confirm = values_confirmation(self.answers['line_of_sight'])
    
        return confirmation_condition(confirm, self.answers['line_of_sight'], values_list=['LOS', 'NLOS'])


class ConditionalInput:

    def __init__(self):

        self.answers = None
        self.line_of_sight = None
        self.scenario = None


    def get_input(self):
        
        if self.line_of_sight == "LOS":

            self.questions = [
                inquirer.Text('h_bs', message="Enter the height of the base station (m)",validate=validate_number),
                inquirer.Text('h_ms', message="Enter the height of the mobile station (m)",validate=validate_number),
            ]
        
        elif self.line_of_sight == "NLOS":

            if self.scenario == "B1":

                self.questions = [
                    inquirer.Text('h_bs', message="Enter the height of the base station (m)",validate=validate_number),
                    inquirer.Text('h_ms', message="Enter the height of the mobile station (m)",validate=validate_number),
                    inquirer.Text('d1', message="Enter length of the street rectangular grid(m)",validate=validate_number),
                    inquirer.Text('d2', message="Enter width of the street rectangular grid(m)",validate=validate_number),
                    inquirer.Text('w', message="Enter total width of the street(m)",validate=validate_number),
                ]
            
            else:

                self.questions = [
                    inquirer.Text('h_bs', message="Enter the height of the base station (m)",validate=validate_number),
                    inquirer.Text('h_ms', message="Enter the height of the mobile station (m)",validate=validate_number),
                ]

        self.answers = inquirer.prompt(self.questions)
        confirm = values_confirmation(self.answers)
    
        return confirmation_condition(confirm, self.answers)


class SaveResultsMenu:

    def __init__(self):

        self.answers = None
        self.questions = [
            inquirer.List('save_results_menu', message="Choose an option", choices=['Save results', 'Do not save results'])
        ]


    def get_input(self):

        self.answers = inquirer.prompt(self.questions)
        return self.answers['save_results_menu']


    def choose_measurement_set(self, measurements_sets_list: list):

        questions = [
            inquirer.Checkbox('measurements_set', message="Choose a measurement set", choices=measurements_sets_list)
        ]
        answers = inquirer.prompt(questions)

        return answers['measurements_set']


def measurement_set_input():
    
    questions = [
        inquirer.Text('measurement_set_name', message="Enter the name of the measurement set", validate=validate_name)
    ]
    asnwer = inquirer.prompt(questions)

    return asnwer['measurement_set_name']


def custom_error_message(message: str):

    clear_screen()
    questions = [
        inquirer.Text('error', message=message)
    ]
    inquirer.prompt(questions)


def clear_screen():

    if name == 'nt':
        system('cls')

    else:
        system('clear')


def confirmation_condition(confirmation_choice, answers, values_list=None):

    if confirmation_choice == 'Next':
        return answers
    
    elif confirmation_choice == 'Back':
        return 'Back'

    elif confirmation_choice == 'Edit values':

        if isinstance(answers, dict):
            return values_input_edit(answers)
        
        else:
            return list_input_edit(values_list)
    
    elif confirmation_choice == 'Main menu':
        return 'Main menu'


def values_confirmation(values):

    clear_screen()

    if isinstance(values, dict):
        for key, value in values.items():
            print(f"{key}: {value}")
    
    else:
        print(f"Current answer: {values}")

    questions = [
        inquirer.List('confirm', message="Do you want to confirm the values?", 
                      choices=['Next', 'Back', 'Edit values', 'Main menu'])
    ]
    answers = inquirer.prompt(questions)

    return answers['confirm']


def values_input_edit(values):

    clear_screen()

    questions = [
        inquirer.Checkbox('values', message="Choose values to edit", choices=[key for key in values.keys()])
    ]

    answers = inquirer.prompt(questions)

    for key in answers['values']:

        if key == 'measurement_name':
            questions = [
                inquirer.Text(key, message=f"Enter the new value for {key}", default=values[key])
            ]

        else:
            questions = [
                inquirer.Text(key, message=f"Enter the new value for {key}", default=values[key], validate=validate_number)
            ]
        
        new_values = inquirer.prompt(questions)
        values[key] = new_values[key]
    
    return values


def list_input_edit(values):

    clear_screen()

    questions = [
        inquirer.List('values', message="Choose value again", choices=values)
    ]

    answers = inquirer.prompt(questions)

    return answers['values']
    

def validate_path(value, answers_dict):

    clear_screen()

    if not answers_dict:
        raise inquirer.errors.ValidationError(reason="Path cannot be empty", value=answers_dict)
    
    if not answers_dict.endswith('.obj'):
        raise inquirer.errors.ValidationError(reason="Path must end with .obj", value=answers_dict)
    
    try:
        open(answers_dict, 'a').close()

    except:
        raise inquirer.errors.ValidationError(reason="Path is not valid", value=answers_dict)
    
    return True


def validate_number(value, answers_dict):

    clear_screen()
    try:

        if str(answers_dict).isdigit():
            return True
        
        float(str(answers_dict))

        if float(str(answers_dict)) < 0:
            raise inquirer.errors.ValidationError(reason="Please input positive value", value=answers_dict)
        
        return True
    except ValueError:
        raise inquirer.errors.ValidationError(reason="Please enter a number", value=answers_dict)


def validate_round(value, answers_dict):

    clear_screen()
    try:
        int(str(answers_dict))
        return True
    
    except ValueError:
        raise inquirer.errors.ValidationError(reason="Please enter an integer number", value=answers_dict)
    

def validate_name(value, answer):

    if not answer:
        raise inquirer.errors.ValidationError(reason="Name cannot be empty", value=answer)
    
    return True


def height_of_stations_input():

    clear_screen()
    questions = [

        inquirer.Text('h_bs', message="Enter the height of the base station (m)",validate=validate_number),
        inquirer.Text('h_ms', message="Enter the height of the mobile station (m)",validate=validate_number)
    ]
    answers = inquirer.prompt(questions)
    confirm = values_confirmation(answers)
    correct_ans = confirmation_condition(confirm, answers)

    return (float(correct_ans['h_bs']), float(correct_ans['h_ms']))


def nlos_b1_input():

    clear_screen()
    questions = [

        inquirer.Text('h_bs', message="Enter the height of the base station (m)",validate=validate_number),
        inquirer.Text('h_ms', message="Enter the height of the mobile station (m)",validate=validate_number),
        inquirer.Text('d1', message="Enter length of the street rectangular grid(m)",validate=validate_number),
        inquirer.Text('d2', message="Enter width of the street rectangular grid(m)",validate=validate_number),
        inquirer.Text('w', message="Enter total width of the street(m)",validate=validate_number),
    ]
    answers = inquirer.prompt(questions)

    return (float(answers['h_bs']), float(answers['h_ms']),
             float(answers['d1']), float(answers['d2']), 
             float(answers['w']))


def calculation_menu():

    clear_screen()
    questions = [
        inquirer.List('calculation_menu', message="Choose an option", choices=['Single calculation', 'Create new measurement set', 'Back'])
    ]
    answers = inquirer.prompt(questions)

    return answers['calculation_menu']
