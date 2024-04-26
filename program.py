from menus import (main_menu, calculation_menu, 
                    ScenarioInput, DefaultValuesInput,
                    LineOfSightInput, MenuEngine)
from calculations import WinnerCalculator

if __name__ == "__main__":
    
    while True:

        choice = main_menu()

        if choice == "Calculate Winner Model":

            def_values = DefaultValuesInput()
            scenario = ScenarioInput()
            line_of_sight = LineOfSightInput()
            calc_menu_engine = MenuEngine(def_values, scenario, line_of_sight)

            if calc_menu_engine.run_menus():
                pass

            else:
                continue

            # if def_values == 'Main menu':
            #     continue

            # elif def_values == 'Back':
            #     continue

            # scenario = scenario_input()
            # if def_values == 'Main menu':
            #     continue

            # elif def_values == 'Back':
            #     def_values.edit_input()
            
            # line_of_sight = line_of_sight_input()

            calc = WinnerCalculator(str(def_values['measurement_name']), scenario, line_of_sight, 
                                    float(def_values['frequency']), float(def_values['distance']), 
                                    int(def_values['res_round']))
            print(calc)
            input()

        elif choice == "Measurement sets":
            pass

        elif choice == "Exit":
            break
