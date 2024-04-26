from menus import (main_menu, calculation_menu, 
                    scenario_input, line_of_sight_input, 
                    default_values_input)
from calculations import WinnerCalculator

if __name__ == "__main__":
    
    while True:

        choice = main_menu()

        if choice == "Calculate Winner Model":

            def_values = default_values_input()

            if def_values == 'Main menu':
                continue

            elif def_values == 'Back':
                continue

            scenario = scenario_input()
            line_of_sight = line_of_sight_input()

            calc = WinnerCalculator(def_values['measurement_name'], scenario, line_of_sight, 
                                    float(def_values['frequency']), float(def_values['distance']), 
                                    int(def_values['res_round']))
            print(calc)
            input()

        elif choice == "Measurement sets":
            pass

        elif choice == "Exit":
            break
