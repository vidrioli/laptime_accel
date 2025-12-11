import pytest
from laptime_accel.src.CarCreate import create_car , Predefined_Cars
from runLapTime import Solver, get_integrator, Euler, RK4


def test_create_car():
    test_car = create_car('CTU24')
    assert test_car.name == 'CTU24'
    assert test_car.m == Predefined_Cars['CTU24']['m']
    assert test_car.Fd(1) > 0
    assert test_car.Frr() > 0
    assert test_car.Fdown(1,1) > 0 and test_car.Fdown(1,1) < 1000
    assert test_car.Favailable(100) * 100 /1000 == test_car.P_max
    with pytest.raises(ValueError):
        create_car('NonExistentCar')


def test_integrator():
    euler = get_integrator('euler')
    rk4 = get_integrator('rk4')
    assert isinstance(euler, Euler) # check if returned object is instance of Euler integrator class
    assert isinstance(rk4, RK4) #same for RK4
    with pytest.raises(ValueError):
        get_integrator('unknown')  # should raise ValueError for unknown integrator type
    assert euler.integrate(lambda y,a: y + a, 1, 0, 1, 2) == 4  

