import inquirer
import inquirer.errors
from os import name, system

def clear_screen():

    if name == 'nt':
        system('cls')

    else:
        system('clear')


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


def los_data_input():

    clear_screen()
    questions = [

        inquirer.Text('h_bs', message="Enter the height of the base station (m)",validate=validate_number),
        inquirer.Text('h_ms', message="Enter the height of the mobile station (m)",validate=validate_number)
    ]
    answers = inquirer.prompt(questions)

    return answers


def scenario_input():

    clear_screen()
    questions = [
        inquirer.List('scenario', message="Choose a scenario", choices=['B1', 'C2', 'D1'])
    ]
    answers = inquirer.prompt(questions)

    return answers['scenario']


def line_of_sight_input():

    questions = [
        inquirer.List('line_of_sight', message="Choose a line of sight", choices=['LOS', 'NLOS'])
    ]
    answers = inquirer.prompt(questions)

    return answers['line_of_sight']


def default_values_input():

    questions = [
        inquirer.Text('measurement_name', message="Enter the name of the measurement"),
        inquirer.Text('frequency', message="Enter the frequency (GHz)",validate=validate_number),
        inquirer.Text('distance', message="Enter the distance (m)",validate=validate_number),
        inquirer.Text('res_round', message="Enter the number of decimal places to round the result",validate=validate_round)
    ]
    answers = inquirer.prompt(questions)

    return answers


def main_menu():

    clear_screen()
    questions = [
        inquirer.List('main_menu', message="WINNER II Calculator (choose an option using arrow keys)", 
                      choices=['Calculate Winner Model', 'Measurement sets','Exit'])
    ]
    answers = inquirer.prompt(questions)

    return answers['main_menu']




def calculation_menu():

    clear_screen()
    questions = [
        inquirer.List('calculation_menu', message="Choose an option", choices=['Single calculation', 'Create new measurement set', 'Back'])
    ]
    answers = inquirer.prompt(questions)

    return answers['calculation_menu']
