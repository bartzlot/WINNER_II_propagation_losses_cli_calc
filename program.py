from menus import (main_menu, calculation_menu, 
                    ScenarioInput, DefaultValuesInput,
                    LineOfSightInput, MenuEngine,
                    ConditionalInput)
from calculations import WinnerCalculator

if __name__ == "__main__":
    
    while True:

        choice = main_menu()

        if choice == "Calculate Winner Model":

            def_values = DefaultValuesInput()
            scenario = ScenarioInput()
            line_of_sight = LineOfSightInput()
            conditionals = ConditionalInput()
            calc_menu_engine = MenuEngine(def_values, scenario, line_of_sight, conditionals)
            
            

            if calc_menu_engine.run_menus():
                pass

            else:
                continue
            
            if scenario.answers['scenario'] == 'B1' and line_of_sight.answers['line_of_sight'] == 'NLOS':
                calc = WinnerCalculator(str(def_values.answers['measurement_name']), scenario.answers['scenario'], 
                                        line_of_sight.answers['line_of_sight'], float(def_values.answers['frequency']), 
                                        float(def_values.answers['distance']), int(def_values.answers['res_round']), 
                                        float(conditionals.answers['h_bs']),float(conditionals.answers['h_ms']), 
                                        float(conditionals.answers['d1']), float(conditionals.answers['d2']), 
                                        float(conditionals.answers['w']))
            
            else:
                calc = WinnerCalculator(str(def_values.answers['measurement_name']), scenario.answers['scenario'], 
                                        line_of_sight.answers['line_of_sight'], float(def_values.answers['frequency']), 
                                        float(def_values.answers['distance']), int(def_values.answers['res_round']), 
                                        float(conditionals.answers['h_bs']),float(conditionals.answers['h_ms']))
            print(calc)
            input()

        elif choice == "Measurement sets":
            pass

        elif choice == "Exit":
            break
