from menus import (main_menu,ScenarioInput, DefaultValuesInput,
                    LineOfSightInput, MenuEngine,
                    ConditionalInput, MeasurementsSetMenu,
                    MeasurementsViewMenu, SaveResultsMenu, 
                    clear_screen, DatabaseOptionsMenu, 
                    measurement_set_input)
from calculations import WinnerCalculator
from database import Database, MeasurementSet
from os.path import exists
import os


if __name__ == "__main__":


    database_path = Database.load_database_path()

    if exists(database_path):

        database = Database.load_database(database_path)
        database.database_path = database_path

    else:
        database = Database()

    measurements_set_menu = MeasurementsSetMenu(database)

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
                
                if not database.measurements_sets_list:

                    measurement_set = MeasurementSet(measurement_set_input())
                    database.add_measurement_set(measurement_set)

                chosen_measurement_sets = save_results.choose_measurement_set(database.measurements_sets_list)

                for measurement_set in chosen_measurement_sets:

                    measurement_set.add_measurement(calc)

            else:
                pass

        elif choice == "Measurement sets":

            measurements_view_menu = MeasurementsViewMenu()
            measurements_menu_engine = MenuEngine(measurements_set_menu, measurements_view_menu)
            measurements_menu_engine.run_menus()
            database.save_database()

        elif choice == "Database options":

            database_menu = DatabaseOptionsMenu(database.database_path)
            ans = database_menu.get_input()

            if ans == "Edit database path":

                new_path = database_menu.new_path_input()
                database.delete_database()
                database.change_database_path(new_path)
                database.save_database()
            
            elif ans == "Create new database":

                new_path = database_menu.new_path_input()
                database.save_database()
                database = Database()
                database.change_database_path(new_path)
                measurements_set_menu.update_database(database)
            
            elif ans == 'Switch Database':

                new_path = database_menu.new_path_input()
                database.save_database()
                database = Database.switch_database(new_path)
                database.change_database_path(new_path)
                measurements_set_menu.update_database(database)

        elif choice == "Exit":

            database.save_database()
            break
