import inquirer
import inquirer.errors

def validate_number(value, answers_dict):
    try:

        if str(answers_dict).isdigit():
            return True
        
        float(str(answers_dict))

        if float(str(answers_dict)) < 0:
            raise inquirer.errors.ValidationError(reason="Please input positive value", value=answers_dict)
        
        return True
    except ValueError:
        raise inquirer.errors.ValidationError(reason="Please enter a number", value=answers_dict)


def los_data_input():
    questions = [

        inquirer.Text('h_bs', message="Enter the height of the base station (m)",validate=validate_number),
        inquirer.Text('h_ms', message="Enter the height of the mobile station (m)",validate=validate_number)
    ]
    answers = inquirer.prompt(questions)

    return answers



