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

    def __init__(self, measure_name: str, scenario: str, line_of_sight: str,frequency, 
                 distance, res_round):
        
        if not isinstance(measure_name, str):
            raise ValueError("measure_name must be a string")
        if not isinstance(scenario, str):
            raise ValueError("scenario must be a string")
        if not isinstance(line_of_sight, str):
            raise ValueError("line_of_sight must be a string")
        
        self.measure_name = measure_name
        self.scenario = scenario
        self.line_of_sight = line_of_sight
        self.frequency = frequency
        self.distance = distance
        self.round = res_round
        self.result = self.calculate_winner_model()


    def __str__(self):
        
        return f"{self.result}"


    def calculate_winner_model(self):

        if self.line_of_sight == "LOS":

            if self.scenario == "B1": 

                
                h_bs = 10
                h_ms = 1.5
                d_bp = 4 * h_bs * h_ms * self.frequency / (3 * 10**8)

                #option 1: 10m< d < d_bp

                return round(self.scenario['B1']['A'] * math.log10(self.distance)
                             + self.scenario['B1']['B'] + self.scenario['B1']['C'] 
                             * math.log10(self.frequency/5), self.round)

                #option 2: d_bp < d < 5km

                return round(40 * math/log10(self.distance) + 9.45 - 17.3 * math.log10(h_bs)
                            - 17.3 * math.log10(h_ms) + 2.7 * math.log10(self.frequency/5), self.round)
            
            elif self.scenario == "C2":  

                d = 20
                h_bs = 25
                h_ms = 1.5
                d_bp = 4 * h_bs * h_ms * self.frequency / (3 * 10**8)

                #option 1: 10m < d < d_bp

                return round(self.scenario['C2']['A'] * math.log10(self.distance)
                             + self.scenario['C2']['B'] + self.scenario['C2']['C'] 
                             * math.log10(self.frequency/5), self.round)
              
                #option 2: d_bp < d < 5km

                return round(40 * math.log10(self.distance) + 13.47 - 14 * math.log10(h_bs)
                            - 14 * math.log10(h_ms) + 6 * math.log10(self.frequency/5), self.round)

            elif self.scenario == "D1": 

                d = 20
                h_bs = 32
                h_ms = 1.5
                d_bp = 4 * h_bs * h_ms * self.frequency / (3 * 10**8)
                
                #option 1: 30m < d < d_bp

                return round(self.scenario['D1']['A'] * math.log10(self.distance)
                             + self.scenario['D1']['B'] + self.scenario['D1']['C'] 
                             * math.log10(self.frequency/5), self.round)
              
            
                #option 2: d_bp < d < 5km

                return round(40 * math.log10(self.distance) + 10.5 - 18.5 * math.log10(h_bs)
                            - 18.5 * math.log10(h_ms) + 1.5 * math.log10(self.frequency/5), self.round)    
                
        elif self.line_of_sight == "NLOS":
            
            if self.scenario == "B1": #10m < d1 < 5km, w/2 < d2 < 2km,

                w = 20
                d1 = 2
                d2 = 4
                h_bs = 10
                h_ms = 1.5

                pl_los = (40 * math.log10(d1) + 9.45 - 17.3 * math.log10(h_bs) - 
                          17.3 * math.log10(h_ms) + 2.7 * math.log10(self.frequency/5))
                
                nj_d1_d2 = max(2.8 - 0.0024 * d1, 1.84)
                # 0 < d2 , w/2 pl_los is applided to pl_nlos
                pl_d1_d2 = pl_los + 20 - 12.5 * nj_d1_d2 + 10 * nj_d1_d2 * math.log10(d2) + 3 * math.log10(self.frequency/5)

                pl_los = (40 * math.log10(d2) + 9.45 - 17.3 * math.log10(h_bs) - 
                          17.3 * math.log10(h_ms) + 2.7 * math.log10(self.frequency/5))
                
                pl_d2_d1 = pl_los + 20 - 12.5 * nj_d1_d2 + 10 * nj_d1_d2 * math.log10(d1) + 3 * math.log10(self.frequency/5)

                return round(min(pl_d1_d2, pl_d2_d1), self.round)

            elif self.scenario == "C2":  #50m < d < 5km

                d = 20
                h_bs = 25
                h_ms = 1.5

                return round((44.9 - 6.55 * math.log10(h_bs)) * math.log10(d) 
                             + 34.46 + 5.83 * math.log10(h_bs) + 23.3 
                             * math.log10(self.frequency/5), self.round)

            elif self.scenario == "D1": #50m < d < 5km

                d = 20
                h_bs = 32
                h_ms = 1.5

                return round(25.11 * math.log10(d) + 55.4 - 0.13 * math.log10(h_bs - 25) 
                             * math.log10(d/100) - 0.9 * math.log10(h_ms - 1.5) + 21.3 
                             * math.log10(self.frequency/5), self.round)

calc = WinnerCalculator("Winner", "B1", "LOS", 2.4, 10, 2)
print(calc)
    

    

        


        
