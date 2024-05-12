from menus import (main_menu, calculation_menu, 
                    ScenarioInput, DefaultValuesInput,
                    LineOfSightInput, MenuEngine,
                    ConditionalInput, MeasurementsSetMenu,
                    MeasurementsViewMenu, SaveResultsMenu, clear_screen)
from calculations import WinnerCalculator
from database import Database, MeasurementSet

if __name__ == "__main__":

    database = Database()

    while True:

        choice = main_menu()

        if choice == "Calculate Winner Model":

            def_values = DefaultValuesInput()
            scenario = ScenarioInput()
            line_of_sight = LineOfSightInput()
            conditionals = ConditionalInput()
            save_results = SaveResultsMenu()
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
            clear_screen()
            print(calc)
            
            choice = save_results.get_input()

            if choice == 'Save results':
                
                chosen_measurement_sets = save_results.choose_measurement_set(database.measurements_sets_list)
                for measurement_set in chosen_measurement_sets:

                    measurement_set.add_measurement(calc)

            else:
                pass

        elif choice == "Measurement sets":

            measurements_set_menu = MeasurementsSetMenu(database)
            measurements_view_menu = MeasurementsViewMenu()
            measurements_menu_engine = MenuEngine(measurements_set_menu, measurements_view_menu)
            measurements_menu_engine.run_menus()

        elif choice == "Exit":
            break
