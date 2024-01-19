from house import House
from room import Room
from window import Window
from heater import Heater

if __name__=="__main__":
    rooms = {"I": Room(0, 50, 0, 40), "II": Room(0, 35, 40, 100), "III": Room(35, 60, 40, 100),
             "IV": Room(60, 100, 40, 80), "V": Room(60, 100, 80, 100)}
    windows = [Window(False, 75, 15, 0), Window(False, 50, 15, 0), Window(False, 10, 20, 0), 
               Window(True, 10, 15, 100), Window(True, 40, 15, 100), Window(True, 70, 20, 100),
               Window(False, 50, 20, 100), Window(True, 15, 20, 0)]
    heaters = [Heater(False, 65, 10, 1), Heater(False, 15, 10, 1), Heater(False, 45, 15, 59),
               Heater(False, 55, 10, 99), Heater(False, 85, 10, 99), Heater(True, 20, 10, 99), Heater(True, 75, 10, 41), Heater(True, 20, 10, 1)]
    params = {"rooms": rooms, "windows": windows,"heaters": heaters}
    home = House(params)
    home.show()
