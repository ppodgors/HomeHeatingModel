import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class House:
    def __init__(self,params):
        self.params = params
        self.matrix= {}
        self.home = np.zeros((101,101))
        self.build_result_matrix()
    def build_partial_matrices(self):
        for key, room in self.params["rooms"].items():
           self.matrix[key] = np.zeros((room.x_len(), room.y_len()))

    def build_result_matrix(self):
        for key, room in self.params["rooms"].items():
            self.home[room.x_min():room.x_max(), room.y_min():room.y_max()] = 1
            self.home[room.x_min(), room.y_min():room.y_max()]=2
            self.home[room.x_max(), room.y_min():room.y_max()]=2
            self.home[room.x_min():room.x_max(), room.y_min()]=2
            self.home[room.x_min():room.x_max(), room.y_max()]=2
        for window in self.params["windows"]:
            if window.is_horizontal():
                y_min, y_max, x = window.coordinates()
                self.home[x, y_min:y_max] = 3
            else:
                x_min, x_max, y = window.coordinates()
                self.home[x_min:x_max, y] = 3
        for heater in self.params["heaters"]:
            if heater.is_horizontal():
                y_min, y_max, x = heater.coordinates()
                self.home[x, y_min:y_max] = 4
            else:
                x_min, x_max, y = heater.coordinates()
                self.home[x_min:x_max, y] = 4


    def show(self):
        cmapmine = ListedColormap(['lightgray','white','black','dodgerblue', 'red'], N=5)
        plt.imshow(self.home,cmap=cmapmine)
        plt.show()

 