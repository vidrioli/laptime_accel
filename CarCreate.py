

class Car:
    def __init__(self,name,m,CdA,P,mu_x,rr):
        self.name = name # car name
        self.m = m       # [kg] mass 
        self.CdA = CdA   # [m^2] aerodynamic drag coeff. * frontal area 
        self.P = P       # [kW] Maximum system power
        self.mu_x = mu_x # [-] longitudinal tire friction coefficient
        self.rr = rr     # [-] tire rolling resistance coefficient

    def __str__(self):
        return(f"""{self.name} vehicle with parameters:
              Mass: {self.m} kg
              Aerodynamic Drag Coefficient * Frontal Area: {self.CdA} m^2
              Maximum System Power: {self.P} kW
              Longitudinal Tire Friction Coefficient: {self.mu_x}
              Tire Rolling Resistance Coefficient: {self.rr}
            """) 


# Dictionary with predefined cars and their parameters
Predefined_Cars = {
    'CTU24': {'name': 'CTU24', 'm': 300, 'CdA': 1.2, 'P': 80, 'mu_x': 1.5, 'rr': 0.015},
    'CTU25': {'name': 'CTU25', 'm': 250, 'CdA': 1.3, 'P': 80, 'mu_x': 1.6, 'rr': 0.015}
}

def create_car(car_name):
    if car_name in Predefined_Cars:         # check if car_name is in predefined cars
        params = Predefined_Cars[car_name]  # get parameters from dictionary
        print(Car(**params))                # print car description
        return Car(**params)                # create instance of Car object, **unpacks dictionary to parametername=value...
                   
    else:
        raise ValueError(f"Car '{car_name}' not found. Choose from {list(Predefined_Cars.keys())}")

        
#print('CTU24' in Predefined_Cars)
#print(Predefined_Cars['CTU24'])
#print(Car(**Predefined_Cars['CTU24']).describe())
