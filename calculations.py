import math


class WinnerCalculator():

    scenarios = {
        "B1": {
            'A': 22.7,
            'B': 41,
            'C': 20
        },
        "C2": {
            'A': 26,
            'B': 39,
            'C': 20
        },
        "D1": {
            'A': 21.5,
            'B': 44.2,
            'C': 20
        }
    }

    def __init__(self, measurement_name: str, scenario: str, line_of_sight: str,frequency, 
                 distance, res_round, h_bs=None, h_ms=None, d1=None, d2=None, w=None):
        
        if not isinstance(measurement_name, str):
            raise ValueError("measure_name must be a string")
        if not isinstance(scenario, str):
            raise ValueError("scenario must be a string")
        if not isinstance(line_of_sight, str):
            raise ValueError("line_of_sight must be a string")
        
        if h_bs and h_ms and not d1 and not d2 and not w:

            self.measurement_name = measurement_name
            self.scenario = scenario
            self.line_of_sight = line_of_sight
            self.frequency = frequency
            self.distance = distance
            self.round = res_round
            self.h_bs = h_bs
            self.h_ms = h_ms
            self.d1 = None
            self.d2 = None
            self.w = None
            self.result = self.calculate_winner_model()
        
        elif h_bs and h_ms and d1 and d2 and w:

            self.measurement_name = measurement_name
            self.scenario = scenario
            self.line_of_sight = line_of_sight
            self.frequency = frequency
            self.distance = distance
            self.round = res_round
            self.h_ms = h_ms
            self.h_bs = h_bs
            self.d1 = d1
            self.d2 = d2
            self.w = w
            self.result = self.calculate_winner_model()
        
        else:
            raise ValueError("Missing input values")


    def __str__(self):

        headers = ["Calculation name", "Scenario", "Line of sight", "Frequency", "Distance", 
                "Heigth of Base Station", "Heigth of Media Station", "Length of Grid(d1)", "Width of Grid(d2)", "Street Width(w)", "Result"]
        values = [self.measurement_name, self.scenario, self.line_of_sight, 
                f"{self.frequency} GHz", f"{self.distance} m", f"{self.h_bs} m", 
                f"{self.h_ms} m", f"{self.d1} m", f"{self.d2} m", f"{self.w} m", 
                f"{self.result} dB"]
        
        header_line = ' | '.join(f"{h:<{len(h)}}" for h in headers)
        value_line = ' | '.join(f"{v:<{len(h)}}" for v, h in zip(values, headers))

        return f"{header_line}\n\n{value_line}"
     
    def print_in_list(self):

        headers = ["Calculation name", "Scenario", "Line of sight", "Frequency", "Distance", 
                "Heigth of Base Station", "Heigth of Media Station", "Length of Grid(d1)", "Width of Grid(d2)", "Street Width(w)", "Result"]
        values = [self.measurement_name, self.scenario, self.line_of_sight, 
                f"{self.frequency} GHz", f"{self.distance} m", f"{self.h_bs} m", 
                f"{self.h_ms} m", f"{self.d1} m", f"{self.d2} m", f"{self.w} m", 
                f"{self.result} dB"]
        
        header_line = ' | '.join(f"{h:<{len(h)}}" for h in headers)
        value_line = ' | '.join(f"{v:<{len(h)}}" for v, h in zip(values, headers))

        return f"{value_line}"
    
    
    def export_to_list(self):

        values = [self.measurement_name, self.scenario, self.line_of_sight, 
                self.frequency, self.distance, self.h_bs, 
                self.h_ms, self.d1, self.d2, self.w, 
                self.result]
        
        return values


    def calculate_winner_model(self):

        if self.line_of_sight == "LOS":

            if self.scenario == "B1": 
                
                # h_bs, self.h_ms = height_of_stations_input()
                d_bp = 4 * self.h_bs * self.h_ms * self.frequency / (3 * 10**8)

                #option 1: 10m< d < d_bp
                if self.distance < d_bp and self.distance > 10:

                    return round(self.scenarios['B1']['A'] * math.log10(self.distance)
                                + self.scenarios['B1']['B'] + self.scenarios['B1']['C'] 
                                * math.log10(self.frequency/5), self.round)

                #option 2: d_bp < d < 5km
                elif self.distance > d_bp and self.distance < 5000:

                    return round(40 * math.log10(self.distance) + 9.45 - 17.3 * math.log10(self.h_bs)
                                - 17.3 * math.log10(self.h_ms) + 2.7 * math.log10(self.frequency/5), self.round)
            
            elif self.scenario == "C2":  

                # self.h_bs, self.h_ms = height_of_stations_input()
                d_bp = 4 * self.h_bs * self.h_ms * self.frequency / (3 * 10**8)

                #option 1: 10m < d < d_bp
                if self.distance < d_bp and self.distance > 10:

                    return round(self.scenarios['C2']['A'] * math.log10(self.distance)
                                + self.scenarios['C2']['B'] + self.scenarios['C2']['C'] 
                                * math.log10(self.frequency/5), self.round)
              
                #option 2: d_bp < d < 5km
                elif self.distance > d_bp and self.distance < 5000:

                    return round(40 * math.log10(self.distance) + 13.47 - 14 * math.log10(self.h_bs)
                                - 14 * math.log10(self.h_ms) + 6 * math.log10(self.frequency/5), self.round)

            elif self.scenario == "D1": 

                # self.h_bs, self.h_ms = height_of_stations_input()
                d_bp = 4 * self.h_bs * self.h_ms * self.frequency / (3 * 10**8)
                
                #option 1: 30m < d < d_bp
                if self.distance < d_bp and self.distance > 30:

                    return round(self.scenarios['D1']['A'] * math.log10(self.distance)
                                + self.scenarios['D1']['B'] + self.scenarios['D1']['C'] 
                                * math.log10(self.frequency/5), self.round)
              
            
                #option 2: d_bp < d < 5km
                elif self.distance > d_bp and self.distance < 5000:

                    return round(40 * math.log10(self.distance) + 10.5 - 18.5 * math.log10(self.h_bs)
                                - 18.5 * math.log10(self.h_ms) + 1.5 * math.log10(self.frequency/5), self.round)    
                
        elif self.line_of_sight == "NLOS":
            
            if self.scenario == "B1": #10m < self.d1 < 5km, self.w/2 < self.d2 < 2km,
                
                
                # self.h_bs, self.h_ms, self.d1, self.d2, self.w = nlos_b1_input()
                nj_d1_d2 = max(2.8 - 0.0024 * self.d1, 1.84)
                nj_d2_d1= max(2.8 - 0.0024 * self.d2, 1.84)
                # 0 < self.d2 , self.w/2 pl_los is applided to pl_nlos
                if self.d2 > 0 and self.d2 < (self.w/2):

                    pl_los = (40 * math.log10(self.d1) + 9.45 - 17.3 * math.log10(self.h_bs) - 
                            17.3 * math.log10(self.h_ms) + 2.7 * math.log10(self.frequency/5))
                    
                    pl_d1_d2 = pl_los + 20 - 12.5 * nj_d1_d2 + 10 * nj_d1_d2 * math.log10(self.d2) + 3 * math.log10(self.frequency/5)

                    pl_los = (40 * math.log10(self.d2) + 9.45 - 17.3 * math.log10(self.h_bs) - 
                            17.3 * math.log10(self.h_ms) + 2.7 * math.log10(self.frequency/5))
                    
                    pl_d2_d1 = pl_los + 20 - 12.5 * nj_d2_d1 + 10 * nj_d2_d1 * math.log10(self.d1) + 3 * math.log10(self.frequency/5)

                    return round(min(pl_d1_d2, pl_d2_d1), self.round)

                else: 

                    pl_d1_d2 = 20 - 12.5 * nj_d1_d2 + 10 * nj_d1_d2 * math.log10(self.d2) + 3 * math.log10(self.frequency/5)
                    
                    pl_d2_d1 = 20 - 12.5 * nj_d1_d2 + 10 * nj_d1_d2 * math.log10(self.d1) + 3 * math.log10(self.frequency/5)

                    return round(min(pl_d1_d2, pl_d2_d1), self.round)
                
            elif self.scenario == "C2":  #50m < d < 5km

                # self.h_bs, self.h_ms = height_of_stations_input()

                return round((44.9 - 6.55 * math.log10(self.h_bs)) * math.log10(self.distance) 
                             + 34.46 + 5.83 * math.log10(self.h_bs) + 23.3 
                             * math.log10(self.frequency/5), self.round)

            elif self.scenario == "D1": #50m < d < 5km

                # self.h_bs, self.h_ms = height_of_stations_input()

                return round(25.11 * math.log10(self.distance) + 55.4 - 0.13 * math.log10(self.h_bs - 25) 
                             * math.log10(self.distance/100) - 0.9 * math.log10(self.h_ms - 1.5) + 21.3 
                             * math.log10(self.frequency/5), self.round)


    

    

        


        
