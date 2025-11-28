import numpy as np

class Car:
    def __init__(self,name,m,CoGz,WB,wd,CdA,ClA,CoP,P_max,mu_x,mu_x_grad,Rl,rr,gear_res,M_max,i):
        self.name = name             # car name
        self.m = m                   # [kg] mass 
        self.CoGz = CoGz             # [m] height of center of gravity
        self.WB = WB                 # [m] wheelbase
        self.wd = wd                 # [-] weight distribution as % of load on front axle (0-1)
        self.CdA = CdA               # [m^2] aerodynamic drag coeff. * frontal area 
        self.ClA = ClA               # [m^2] aerodynamic lift coeff. * frontal area
        self.CoP = CoP               # [-] aerodynamic ceter of pressure as percentage on front axle (0-1)
        self.P_max = P_max           # [kW] Maximum system power
        self.mu_x = mu_x             # [-] longitudinal tire friction coefficient at 0N Fz
        self.mu_x_grad = mu_x_grad   # [-] gradient of longitudinal tire friction coefficient per N of Fz
        self.Rl = Rl                 # [m] Tire LOADED radius
        self.rr = rr                 # [-] tire rolling resistance coefficient
        self.gear_res = gear_res     # [-] gearbox resistance coefficient  
        self.M_max = M_max           # [Nm] maximum individual motor torque
        self.i = i                   # [-] planet gearbox gear ratio as i:1

    def __str__(self):       #""" used to print into new lines"   
        return(f"""{self.name} vehicle with parameters: 
              Mass: {self.m} kg
              Aerodynamic Drag Coefficient * Frontal Area: {self.CdA} m^2
              Maximum System Power: {self.P_max} kW
              Longitudinal Tire Friction Coefficient: {self.mu_x}
              Tire Rolling Resistance Coefficient: {self.rr}
              Maximum Individual Motor Torque: {self.M_max} Nm
              Planet Gearbox Gear Ratio: {self.i}:1
              and others...
            """) 
    
    def Fd(self,v,rho=1.016): # calculate aerodynamic drag force on car, default air density at Hockenheimring during August
        return 0.5 * rho * self.CdA * v**2
    
    def Frr(self): # calculate rolling resistance force on car (simplified model)
        return self.m * 9.81 * self.rr
    
    def Fgear(self,v): #calculate gearbox resistance force on car (simplified model)
        return v * self.gear_res
    
    def Fdown(self,v,rho=1.016): #calculate vehicle downforce, default air density at Hockenheimring during August
        return 0.5 * rho * self.ClA * v**2

    def Favailable(self,v): # calculate available tractive force at given speed
        omega_wheel = v / self.Rl  # wheel angular speed [rad/s]
        omega_motor = omega_wheel * self.i  # motor angular speed [rad/s]
        if omega_motor * 4 * self.M_max < self.P_max * 1000: # chceck if torque is power limited for 4 motors
            return 4 * self.M_max * self.i / self.Rl  # total available tractive force from 4 motors before power limit [N]
        else:
            M = (self.P_max * 1000) / (omega_motor*4)  # torque limited by system power
            return 4 * M * self.i / self.Rl  # total available tractive force from 4 motors after power limit [N]       

    def Nf(self,v,a): # calculate normal force on front axle with load transfer and downforce
        Fdown = self.Fdown(v) * self.CoP
        Nf_static = self.m * self.wd * 9.81
        return Nf_static + Fdown - (self.m * a * self.CoGz) / self.WB
    
    def Nr(self,v,a): # calculate normal force on rear axle with load transfer and downforce
        Fdown = self.Fdown(v) * (1 - self.CoP)
        Nr_static = self.m * (1 - self.wd) * 9.81
        return Nr_static + Fdown + (self.m * a * self.CoGz) / self.WB


    def Ftractive(self,v,a): 
        F_avail = self.Favailable(v)
        Nf = self.Nf(v,a)
        Nr = self.Nr(v,a)
        Ff = Nf * (self.mu_x - self.mu_x_grad * (Nf/2))  # maximum tractive force on front axle [N]
        Fr = Nr * (self.mu_x - self.mu_x_grad * (Nr/2))  # maximum tractive force on rear axle [N]
        F_traction_limit = Ff + Fr # maximum tractive force limited by tire friction 
        return min(F_avail, F_traction_limit) # return actual tractive force for entire vehicle [N]
    

#(self,name,m,CoGz,WB,wd,CdA,ClA,CoP,P_max,mu_x,mu_x_grad,Rl,rr,gear_res,M_max,i):
# Dictionary with predefined cars and their parameters
Predefined_Cars = {
    'CTU24': {'name': 'CTU24', 'm': 300, 'CoGz': 0.209, 'WB': 1.53, 'wd': 0.53, 'CdA': 1.2, 'ClA': 5, 'CoP': 0.465, 'P_max': 80, 'mu_x': 1.5, 'mu_x_grad': 7.9e-05, 'Rl': 0.2, 'rr': 0.015, 'gear_res': 0.001, 'M_max': 30, 'i': 12},
    'CTU25': {'name': 'CTU25', 'm': 250, 'CoGz': 0.209, 'WB': 1.53, 'wd': 0.53, 'CdA': 1.3, 'ClA': 6, 'CoP': 0.465, 'P_max': 80, 'mu_x': 1.6, 'mu_x_grad': 7.9e-05, 'Rl': 0.2, 'rr': 0.015, 'gear_res': 0.001, 'M_max': 30, 'i': 12}
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

