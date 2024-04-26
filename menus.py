import inquirer
import inquirer.errors
from os import name, system

def clear_screen():

    if name == 'nt':
        system('cls')

    else:
        system('clear')


def values_confirmation(values):

    clear_screen()

    for key, value in values.items():
        print(f"{key}: {value}")

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


def height_of_stations_input():

    clear_screen()
    questions = [

        inquirer.Text('h_bs', message="Enter the height of the base station (m)",validate=validate_number),
        inquirer.Text('h_ms', message="Enter the height of the mobile station (m)",validate=validate_number)
    ]
    answers = inquirer.prompt(questions)

    return float(answers['h_bs']), float(answers['h_ms'])


def nlos_b1_input():

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

def scenario_input():

    clear_screen()
    choices = ['B1', 'C2', 'D1']
    questions = [
        inquirer.List('scenario', message="Choose a scenario", choices=choices)
    ]
    answers = inquirer.prompt(questions)

    confirm = values_confirmation(answers)

    if confirm == 'Next':
        return answers
    
    elif confirm == 'Back':
        return 'Back'

    elif confirm == 'Edit values':
        return list_input_edit(choices)
    
    elif confirm == 'Main menu':
        return 'Main menu'
    
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
        inquirer.Text('res_round', message="Enter the number of decimal places to round the result",validate=validate_round),
    ]
    answers = inquirer.prompt(questions)
    confirm = values_confirmation(answers)

    if confirm == 'Next':
        return answers
    
    elif confirm == 'Back':
        return 'Back'

    elif confirm == 'Edit values':
        return values_input_edit(answers)
    
    elif confirm == 'Main menu':
        return 'Main menu'
        

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
